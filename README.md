# Test FastAPI APP.

## Stack
FastAPI + SqlAlchemy + Postgres + async support.

## Tests

Some basic API tests with inmemory replacement (sqllite)

## Run

Copy file .env.example to .env and run:

`docker-compose run -p 8000:8000 backend_app` 

It should run two services: postgres and this app. There is one extra service (db_editor).

## Use

Open in browser http://localhost:8080/docs to have access to testable environment. 

## Notes

This isn't production ready!! This repo is result of some experiments with fastapi. 
