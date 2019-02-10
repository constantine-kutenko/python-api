# PostgreSQL 10.3 docker image

PostgreSQL 10.3 database engine.

## Requirements

The image to be built and run requires docker - containerization platform. Check upstream documentation for how to install docker on your system.

## Building

To build an image run following command in application root path

```bash
docker build \
    --pull \
    --tag postgresql-10.3 \
    -f docker/Dockerfile .
```

To run the image use

```bash
docker run \
    --name postgresql \
    --volume /var/lib/pgsql/10/data:/var/lib/pgsql/10/data:rw \
    -p 5432:5432 \
    -itd postgresql-10.3 \
    postgres
```

## Environment variables

| Variable            | Default value   | Description |
| ------------------- | --------------- | ----------- |
| POSTGRESQL_MAJOR      | 10 | Specifies the major version of PostgreSQL server. |
| POSTGRESQL_LISTEN_ADDRESS    | 0.0.0.0 | Specifies an IP address PostgreSQL will start on. This variable is mandatory. |
| POSTGRESQL_LISTEN_PORT       | 5432 | Specifies a TCP port to be binded by PostgreSQL. This variable is mandatory. |
| POSTGRESQL_DATA_DIR   | /var/lib/pgsql/10/data | Specifies a path to PostgreSQL database files. |
| POSTGRESQL_BIN_DIR    | /usr/pgsql-10/bin | Specifies a path to PostgreSQL binary files. |
| POSTGRESQL_USER       | postgres | Specifies a PostgreSQL process owner. |
| POSTGRESQL_GROUP      | postgres | Specifies a PostgreSQL process group. |
| CONTAINER_UID       | 26 | Defines an actual UID will be assigned to PostgreSQL user. |
| CONTAINER_GID       | 26 | Defines an actual GID will be assigned to PostgreSQL group. |
