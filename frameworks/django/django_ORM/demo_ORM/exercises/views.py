from django.shortcuts import render
from .models import Employee
from django.db.models import Q
from django.db import connection


def django_ORM_OR(request):

    # One way to filter

    employees = Employee.objects.filter(firstName__startswith="r") | Employee.objects.filter(lastName__startswith="g")

    # Using Q Objects

    employees = Employee.objects.filter(Q(firstName__startswith="r")|Q(lastName__startswith="g"))

    # Prints performance related stuff

    print(connection.queries)

    return render(request, 'output-OR.html', {"data": employees})


def django_ORM_AND(request):

    # Multiple filter statements

    # employees = Employee.objects.filter(firstName__startswith="r") & Employee.objects.filter(lastName__startswith="g")

    # Multiple Q objects

    employees = Employee.objects.filter(Q(firstName__startswith="r") & Q(lastName__startswith="g"))

    return render(request, "output-AND.html", {"data": employees})