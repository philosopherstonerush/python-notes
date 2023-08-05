# Adding onto class based implementations of views, we can use mixins

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer

# generics are classes that implement a lot of functions that we want already, so we just inherit them.

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions, renderers
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # If the request is not from an authenicated user then just make it readonly
    
    def perform_create(self, serializer): # Overrides the existing create function in ListCreateAPIVIEW to save the user related to the code snippet.
        serializer.save(owner=self.request.user) 


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
    # If the request is not from an authenicated user then just make it readonly. IsOwnerOrReadOnly is custom permission

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# There are two styles of HTML renderer provided by REST framework, one for dealing with HTML rendered using templates, the other for dealing with pre-rendered HTML, which is implemented below

class Snippethighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer] 

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# Single entry point

# reverse function in order to return fully-qualified URLs
# URL names 'user-list' is given for convenience, they are added in urls.py

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request,format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })