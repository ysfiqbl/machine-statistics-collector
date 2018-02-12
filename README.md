# Overview
This application is used to demonstrate how to collect information from a server. 
The application connects to the server via SSH, runs a script to get information and stores the results in a database.
An email will also be fired if a given statistic is above the threshold value. 

The demo uses docker to setup the mock environment.

There are 5 docker containers in total
* Server - is the app server which runs the application. The application uses celery as a task queue to distribute the connections to the client machines.
* Rabbitmq - is used as a message broker for celery
* Database - a MariaDb container for storing persistent data
* Client 1 - an Ubuntu machine that allows SSH connections. This is mock client #1
* Client 2 - an Ubuntu machine that allows SSH connections. This is mock client #2

Please `docker-compose.yml` for more details on each container.

This application can be used on existing Linux machines that allows SSH connections by updating `server/app/config.xml`. This config file contains the client information, credentials and thresholds.


# Pre-requisites
Docker is required to run the application.
The application was tested on 
* Ubuntu 16.04
* Docker 17.06.0-ce build 02c1d87
* Docker Compose 1.14.0 build c7bdf9e


# Running the Application
## Run Docker Containers
* `docker-compose up --build`

## Setup Config File
* `docker network inspect mstats_intranet`

Find the "Containers" key and then update the IPs of client_1 and client_2 in the 
config.xml and config_test.xml file. 

## Creating the Development and Test Database
* `docker-compose exec db bash`
* `cd db_scripts`
* `chmod +x initilaize_db.sh`
* `./initialize_db.sh`

## Initialize Development Database
* `docker-compose exec server alembic downgrade -1`
* `docker-compose exec server alembic upgrade head`

## Running Tests
* `docker-compose exec server pytest app/tests/test_app.py`

## Running Test Coverage
- `docker-compose exec server py.test --cov=app app/tests/`

## Run Application
* `docker-compose exec server python -m app.app`

## Stop Application
* `Ctrl + C`
* `docker-compose stop`


# TODO 
* Add support for Windows servers
* Handle validation
* Handle logging
* Hide client passwords / use SSH keys
