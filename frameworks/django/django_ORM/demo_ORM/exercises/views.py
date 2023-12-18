from django.shortcuts import render
from .models import Employee, Clerks
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


def django_ORM_UNION(request):

    employees = Employee.objects.all().union(Clerks.objects.all())

    return render(request, "output-UNION.html", {'data': employees})

def django_ORM_NOT(request):

    # Use exclude
    employees = Employee.objects.exclude(firstName__startswith="r")

    # Use ~Q
    employees = Employee.objects.filter(~Q(firstName__startswith="r"))

    return render(request, "output-NOT.html", {'data': employees})

def django_ORM_only(request):

    # Take only the firstName column of all records
    employees = Employee.objects.all().only('firstName')

    return render(request, "output-only.html", {'data': employees})

def django_ORM_RAW(request):

    employees = Employee.objects.raw("SELECT * FROM exercises_employee")

    return render(request, "output-RAW.html", {'data':employees})

def django_ORM_bypassORM_SQL(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM exercises_employee")
        employees = dictfetchall(cursor=cursor)
    return render(request, "output-bypassORM.html", {'data': employees})

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]