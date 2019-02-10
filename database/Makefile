
#
#
#

APP_NAME="postgresql"
APP_VERSION="10.3"
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
		--net=host \
		--name ${CONTAINER_NAME} \
		--hostname ${APP_NAME} \
		--volume /var/lib/pgsql/10/data:/var/lib/pgsql/10/data:rw \
		-it ${IMAGE_NAME}:${APP_VERSION} \
		postgres

shell:
	@clear
	@docker run \
		--rm \
		--net=host \
		--name ${CONTAINER_NAME} \
		--hostname ${APP_NAME} \
		--volume /var/lib/pgsql/10/data:/var/lib/pgsql/data:rw \
		-it ${IMAGE_NAME}:${APP_VERSION} \
		/bin/bash
