Contributing to servicenowpy
============================

Contributions of all kinds are welcome.

#### Setting up

servicenowpy repository comes with a simple mock API, developed with FastAPI, that you can use to run quick tests, in case you don't have a ServiceNow Developer instance. However, I strongly recommend you to get one [here](https://developer.servicenow.com/dev.do).

After cloning the repository to your local environment, enter the project directory and copy the file ".example.env" to a file called ".env".
```shell
cd servicenowpy
cp .example.env .env
```
Change the keys `SERVICENOWPY_INSTANCE_URL`, `SERVICENOWPY_USER` and `SERVICENOWPY_PASSWORD` values to your ServiceNow Developer instance values.

#### With Docker

Ensure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

On the project root directory, run:
```shell
docker-compose up -d
```
Now you have two containers running, one is the mock API server and the other has the servicenowpy source code. Get a bash terminal on the servicenowpy one:
```shell
docker exec -it servicenowpy bash
```

#### Without Docker

Inside the project root directory, navigate to the "servicenowpy" directory and install the requirements (Requests library):
```shell
cd servicenowpy
pip3 install -r requirements.txt
```
