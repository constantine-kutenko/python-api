
#
#
#

APP_NAME="python-api"
APP_VERSION="1.0"
IMAGE_NAME="${APP_NAME}"
CONTAINER_NAME="${APP_NAME}-${APP_VERSION}"

all: build run

build:
	@clear
	@docker rmi -f ${IMAGE_NAME} 2>&1 1> /dev/null; exit 0
	@docker build \
		--tag ${IMAGE_NAME}:${APP_VERSION} \
		-f docker/Dockerfile .

run:
	@clear
	@docker run \
		--rm \
		--name ${CONTAINER_NAME} \
		--hostname ${APP_NAME} \
		--net=host \
		-e POSTGRESQL_SERVICE_HOST="192.172.253.49" \
		-e POSTGRESQL_SERVICE_PORT="5432" \
		-e POSTGRESQL_REQUEST_TIMEOUT="3" \
		-e POSTGRESQL_DATABASE_NAME="passengers" \
		-e POSTGRESQL_DATABASE_USER="titanic" \
		-e POSTGRESQL_DATABASE_PASSWORD="" \
		-e APP_ADDRESS="0.0.0.0" \
		-e APP_PORT=5000 \
		-p 5000:5000 \
		-it ${IMAGE_NAME}:${APP_VERSION}

shell:
	@clear
	@docker run \
		--rm \
		--name ${CONTAINER_NAME} \
		--hostname ${APP_NAME} \
		-e POSTGRESQL_SERVICE_HOST="192.172.253.49" \
		-e POSTGRESQL_SERVICE_PORT="5432" \
		-e POSTGRESQL_REQUEST_TIMEOUT="3" \
		-e APP_ADDRESS="0.0.0.0" \
		-e APP_PORT=5000 \
		-p 5000:5000 \
		-it ${IMAGE_NAME}:${APP_VERSION} \
		/bin/sh

application:
	@clear
	@POSTGRESQL_SERVICE_HOST="192.172.253.49" \
		POSTGRESQL_SERVICE_PORT="5432" \
		POSTGRESQL_REQUEST_TIMEOUT="3" \
		POSTGRESQL_DATABASE_NAME="passengers" \
		POSTGRESQL_DATABASE_USER="titanic" \
		POSTGRESQL_DATABASE_PASSWORD="" \
		APP_ADDRESS="0.0.0.0" \
		APP_PORT=5000 \
		python3.6 app/app.py
