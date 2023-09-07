# Description

A simple user CRUD flask App which connects to your mongoDB.

# Pre-requisites  

- Install Docker Desktop.
- Pull mongo image in Docker.
- Run Docker mongo database container.
- Create a database called `user` in mongo.
- create a collection called `userCRUD` in mongo.
- Install python if you haven't already.

# Instructions

1) Install pipenv.
```
pip install pipenv
```
2) Open a terminal window in the project directory.
3) Run `pipenv install`
4) Run flask server
```
flask --app main run
```

# Notes

- SQLAlchemy doesn't support NoSQL databases. Used pyMongo instead.