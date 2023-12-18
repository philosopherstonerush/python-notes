from django.db import models

class Person(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    class Meta:
        abstract = True

class Employee(Person):
    salary = models.IntegerField()

class Clerks(Person):
    typing_speed = models.IntegerField()


