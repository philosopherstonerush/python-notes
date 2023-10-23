# Stuff that I learnt on how to use Django ORM:

## ORM - object relational mapping

Its models your database table and has helpful methods to query your database without having to write raw sql yourself.

To get objects:

```
SELECT * FROM EMPLOYEE

equivalent to

Employee.objects.all()

where employee is your model.

```

## Q Objects

`Q Objects` are used to design complex arguments.

`~Q` used to mean like `NOT` or to exclude. 

## To print the query that happened

```

emps = Employees.objects.all()

print(emps.query)

```

To find performance related information you can also use connection.

```

from django.db import connection

print(connection.queries)


```

## Field Lookups

Theres are suffixes that can be added to your model's fields so you can specify certain effects on them

```

firstName__startswith="r" 

retrieves name that starts with 'r'

```

## ORM OR Query

```

.filter() - helps to filter on parameters.

```

imp - `from django.db.models import Q`

Methods:
1) Use | with multiple filter
2) Use `Q` Objects.



