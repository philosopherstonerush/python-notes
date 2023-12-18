from django.urls import path
from .views import *

urlpatterns = [
    path("output-OR", django_ORM_OR),
    path("output-AND", django_ORM_AND),
    path("output-UNION", django_ORM_UNION),
    path("output-NOT", django_ORM_NOT),
    path("output-only", django_ORM_only),
    path("output-RAW", django_ORM_RAW),
    path("output-bypass", django_ORM_bypassORM_SQL),
]