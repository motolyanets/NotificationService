# Notification Service

## General info
This project is a web application for manage newsletters and get statistics.

## Setup
Change .env-example to .env and use docker-compose.
```
docker-compose build
```
```
docker-compose up
```
Than you need to create migrations:
```
docker-compose exec backend python manage.py makemigrations
```
And apply the migration:
```
docker-compose exec backend python manage.py migrate
```

## Creator
[Andrey Motolyanets](https://github.com/motolyanets)
