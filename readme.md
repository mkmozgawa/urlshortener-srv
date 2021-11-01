# Urlshortener-srv

A Flask service for url shortening.

## Requirements
* Python, pip etc
* Docker & docker-compose

## Setup
1. `docker-compose build`
2. `docker-compose up -d`
3. `docker-compose exec api python manage.py recreate_db`

=> [Swagger](http://localhost:5004)

## Tests
`docker-compose exec api python -m pytest "src/tests"`
