from django.urls import path
from .views import *

urlpatterns = [
    path("output-OR", django_ORM_OR),
    path("output-AND", django_ORM_AND),
]