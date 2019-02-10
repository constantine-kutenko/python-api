# Python API

```python-api``` is a simple application written in Python. It provides a simple REST API to communicate with PostgreSQL database.

## Requirements

The image to be built and run requires Docker - containerization platform. Check upstream documentation for how to install docker on your system.

## Building

To build an image run following command in application root path

```bash
docker build \
    --pull \
    --tag python-api \
    -f docker/Dockerfile .
```

To run the image use the following command

```bash
docker run \
    --rm \
    --name python-api \
    -e POSTGRESQL_SERVICE_HOST="0.0.0.0" \
    -e POSTGRESQL_SERVICE_PORT="5432" \
    -e POSTGRESQL_REQUEST_TIMEOUT="10" \
    -e POSTGRESQL_DATABASE_NAME="passengers" \
    -e POSTGRESQL_DATABASE_USER="titanic" \
    -e POSTGRESQL_DATABASE_PASSWORD="password" \
    -p 5000:5000 \
    -it python-api
```

## Environment variables

| Variable            | Default value   | Description |
| ------------------- | --------------- | ----------- |
| POSTGRESQL_SERVICE_HOST    | 127.0.0.1 | Specifies a database engine IP address to request |
| POSTGRESQL_SERVICE_PORT    | 5432 | Specifies a database engine TCP port |
| POSTGRESQL_DATABASE_NAME   | null | Specifies a name of database to be backed up; The variable is mandatory |
| POSTGRESQL_DATABASE_USER   | null | Specifies a username for a database; The variable is mandatory |
| POSTGRESQL_REQUEST_TIMEOUT | 5 | Specifies a time range between check requests to a database engine |
| APP_ADDRESS                | 0.0.0.0 | Specifies an IP address for application to listen on |
| APP_PORT                   | 5000 | Specifies a TCP port of application to listen on |
