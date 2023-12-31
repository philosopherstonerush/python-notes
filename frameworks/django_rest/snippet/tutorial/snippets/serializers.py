from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


"""

Serializers convert one datatype to another.

These serializers manipulate data in the database. There can be serializers for both request and response.

"""

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={"base_template": "textarea.html"})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")

#     def create(self, validated_data):
#         return snippet.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.code = validated_data.get("code", instance.code)
#         instance.linenos = validated_data.get("linenos", instance.linenos)
#         instance.language = validated_data.get("language", instance.language)
#         instance.save()
#         return instance



"""
the same above code could be replicated with ModelSerializer class (serializer.ModelSerializer)

Relationships between entities could be managed via different ways - like linking users to their snippets. 
1)Using primary keys ---> ModelSerializer is used, id is included by default.
2)Using hyperlinking between entities.
3)Using an unique identifying slug field on the related entity.
4)Using the default string representation of the related entity.
5)Nesting the related entity inside the parent representation.
Some other custom representation.

"""

# Hyperlinking gives us a nice way of browsable api

class SnippetSerializer(serializers.HyperlinkedModelSerializer):

    highlight = serializers.HyperlinkedIdentityField(view_name="snippet-highlight", format="html")

    # This is untyped
    
    owner = serializers.ReadOnlyField(source="owner.username") 
    
    class Meta:
        model = Snippet 
        fields = ["url", "id", "title", "highlight", "code", "linenos", "language", "style", "owner"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name= "snippet-detail", read_only = True)

    class Meta:
        model = User 
        fields = [ "url", "id", "username", "snippets"]

