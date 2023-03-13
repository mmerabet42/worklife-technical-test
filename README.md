# Worklife Python Technical test

This project serves as a technical test for middle-senior backend developers in Python.

It makes use of FastAPI (and Pydantic), SQLAlchemy (orm), alembic (migrations).
It also uses PostgreSQL as database and poetry for dependency management.

## Overview

You are building an employee vacation handling system to manage leave.

Employees belong to teams. There can be many teams. One employee can belong to only one team.

Employee vacations can be of two types:
* Unpaid leave
* Paid leave

A vacation has:
* A type of vacation (as explained above)
* A start date
* An end date

### Notes

For this project:
* There is no half-day leaves, only complete days.
* There is no employee balance.
* Employees work a typical work week of 5/7 with weekends being on Saturday-Sunday

## The project

You need to create an API to help manage vacations including:
* Models and relationships for the various entities
* Features logic (see below)
* API Endpoints

Your API should be able to handle **at least** the following features:
* Create employees (DONE)
* Create, update and delete vacations (DONE)
* Search for employees on vacation given various parameters
* When creating or updating a vacation, if it overlaps (or is contiguous to) another one, merge them into one.
Only works with vacations of the same type, else it will fail (overlaps with another type of vacation). (DONE)

The current boilerplate should serve as a base to start with.
Feel free to upgrade / downgrade it as you see fit.

#### Bonus features
If you have the time/will, you can implement any (or all) of those features:
* Search employees and vacations by employee name/identifier (DONE)
* Searching should also return the number of vacation days for each employee (given the search parameters). (DONE)
* Compare two employees and return the days they will be both on vacation
* Implement a balance, decreasing as an employee takes paid vacations


## What we expect

4 to 5 hours is a good target for this exercice, but you can spend as much or little time as you'd like.

Your answer to this test should be a repository.

Feel free to implement this project in whatever way you feel like, we do not impose any limitations/requirements, 
we simply give you a base to work with.

## Requirements

* docker
* poetry (optional, if you want to add libs)
* make (optional)

## Usage

Depending on your docker and docker-compose setup you might need to use

`docker-compose up -d` or `docker compose up -d`

But you can run the container easily:

`make up`

Run the container, but rebuild the images first:

`make reup`

Print logs:

`make logs`

Stop the container:

`make down`

Create the databases, and migrate:

`make create-db && make migrate-db && make ENV=test create-db && make ENV=test migrate-db`

Run the tests:

`make ENV=test test`

Notice the ENV variable, which specifies the .env file to use (`test` will use `app.test.env` for example)

Once the container is running, you should be able to access the docs at http://localhost:880/docs

To create and migrate the database with the migration already added:

First use `make create-db`

Then use `make migrate-db` (`make ENV=test migrate-db` for the test environment)

If you make modifications/additions to models and want to auto generate migrations you can use. 
Don't forget to migrate the database afterwards.

`make autogenerate-migration revision_message='"your_message"'`

