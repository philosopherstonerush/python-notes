# Stuff that I learnt on how to use Django ORM:

## Tools

Use a GUI Tool to visualize the tables - to make life easier

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

Theres are suffixes that can be added to your model's fields so you can specify certain effects on them.

```

firstName__startswith="r" 

field lookup = __startswith

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


# ORM UNION Query

Make the result the union of two operations.

```

<sql>.union(<sql>)

```

## WATCH OUT!

1) Ordering - if you any kind of ordering present within the meta class of your model, then if you are using sqlite3 ---> Error.

# ORM NOT Query

Two ways:
1) exclude(<condition>)
2) filter(~Q(<condition>)) - Using Q objects

# Select only individual fields

```

.only('<fieldName1>', '<fieldName2>')

```

It only retreives the mentioned fields.

The only() and defer() methods in Django are used to fine-tune the query performance by selecting only the necessary fields or deferring the loading of certain fields until they are actually accessed. By default, Django retrieves all the fields of a model when it queries the database

# Raw Query

```python

.raw() --> send in the raw sql queries

```

You can utilize `translations` - meaning remapping certain fields to a different name through this way.

## WATCH OUT 

The results from the raw sql query execution are deferred models - meaning they are initialized on demand. The necessary fields or deferring the loading of certain fields until they are actually accessed. By default, Django retrieves all the fields of a model when it queries the database

## Raw queries by skipping ORM completely

```python
import django.db.connection

cursor = connection.cursor()
cursor.execute(sql) ---> executes our sql
r = cursor.fetchone() ---> fetches one
r = cursor.fetchall() ---> fetches all the results

or 

with connection.cursor() as cursor:
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

```

For multiple database connections:-

```python

with connections["my_db_alias"].cursor() as cursor:
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

```

### WATCH OUT 

The data returned in Tuples not dictionary! So `.<field-name>` cannot be accessed.

At a small performance and memory cost, you can return results as a dict by using something like this:

```python

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

```