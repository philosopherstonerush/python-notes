from django.urls import path
from snippets import views_func, views_class, views_mixins
from rest_framework.urlpatterns import format_suffix_patterns

# if you are using views as functions

# urlpatterns = [
#     path("snippets/", views_func.snippet_list),
#     path("snippets/<int:pk>/", views_func.snippet_detail)
# ]

# if you are using views as classes

# urlpatterns = [
#     path("snippets/", views_class.SnippetList.as_view()),
#     path("snippets/<int:pk>/", views_class.SnippetDetail.as_view())
# ]

# if you are usings views as mixins

urlpatterns = [
    path('', views_mixins.api_root),
    path('snippets/',
        views_mixins.SnippetList.as_view(),
        name='snippet-list'),
    path('snippets/<int:pk>/',
        views_mixins.SnippetDetail.as_view(),
        name='snippet-detail'),
    path('snippets/<int:pk>/highlight/',
        views_mixins.Snippethighlight.as_view(),
        name='snippet-highlight'),
    path('users/',
        views_mixins.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/',
        views_mixins.UserDetail.as_view(),
        name='user-detail')
]

# For format declaration
urlpatterns = format_suffix_patterns(urlpatterns)