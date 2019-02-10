#!/bin/sh

set -e

# Define mandatory variables
POSTGRESQL_SERVICE_HOST=${POSTGRESQL_SERVICE_HOST:-"127.0.0.1"}
POSTGRESQL_SERVICE_PORT=${POSTGRESQL_SERVICE_PORT:-"5432"}
APP_ADDRESS=${APP_ADDRESS:-"0.0.0.0"}
APP_PORT=${APP_PORT:-"5000"}
if [[ -z "${POSTGRESQL_DATABASE_NAME}" ]]; then echo "The database name must be defined explicitly."; exit 1; fi
if [[ -z "${POSTGRESQL_DATABASE_USER}" ]]; then echo "The database user must be defined explicitly."; exit 1; fi

function wait_sources()
{
  # Define timeout between requests to a database
  if [ -z $1 ]; then POSTGRESQL_REQUEST_TIMEOUT=5; else POSTGRESQL_REQUEST_TIMEOUT=$1; fi

  # Request a database until it's ready to accept connections
  echo -e "Waiting for database on ${POSTGRESQL_SERVICE_HOST}:${POSTGRESQL_SERVICE_PORT}..."
  until nc -z ${POSTGRESQL_SERVICE_HOST} ${POSTGRESQL_SERVICE_PORT}
  do
    echo "PostgreSQL database is unreachable. Sleeping for ${POSTGRESQL_REQUEST_TIMEOUT} seconds."
    sleep ${POSTGRESQL_REQUEST_TIMEOUT}
  done
  
  echo -e "[ OK ] PostgreSQL database"
}

function start_app()
{
  wait_sources
  echo -e "Starting the application on ${APP_ADDRESS}:${APP_PORT}..."
  exec $@
}

case $1 in
  'python')
    start_app $@
  ;;
  *)
    exec $@
  ;;
esac
