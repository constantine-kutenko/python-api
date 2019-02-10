FROM centos:7

#
#
#

ARG POSTGRESQL_MAJOR="10"
ARG POSTGRESQL_DATA_DIR="/var/lib/pgsql/${POSTGRESQL_MAJOR}/data"

ENV POSTGRESQL_MAJOR=${POSTGRESQL_MAJOR} \
    POSTGRESQL_DATA_DIR=${POSTGRESQL_DATA_DIR} \
    POSTGRESQL_BIN_DIR="/usr/pgsql-${POSTGRESQL_MAJOR}/bin" \
    POSTGRESQL_USER="postgres" \
    POSTGRESQL_GROUP="postgres" \
    CONTAINER_UID=26 \
    CONTAINER_GID=26 \
    TZ="UTC"

COPY docker/entrypoint.sh /entrypoint.sh

# Install PostgreSQL Server and Client packages
RUN groupadd -f -g ${CONTAINER_GID} ${POSTGRESQL_GROUP} && \
    useradd -u ${CONTAINER_UID} -g ${CONTAINER_GID} -s /sbin/nologin -M ${POSTGRESQL_USER} && \
    yum update -y && \
    yum install -y --nogpgcheck yum-plugin-ovl && \
    yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm && \
    yum install -y postgresql10-server postgresql10 postgresql10-contrib && \
    yum clean all && \
    rm -rf /var/cache/yum/* && \
    mkdir -p /run/postgresql && \
    chmod +x /entrypoint.sh && \
    chown -R ${POSTGRESQL_USER}:${POSTGRESQL_GROUP} /run/postgresql

WORKDIR ${POSTGRESQL_DATA_DIR}

LABEL name="postgres" \
    description="PostgreSQL is a powerful, open source object-relational database system." \
    maintainer="Constantine Kutenko <constantine.kutenko@gmail.com>" \
    os="CentOS Linux 7" \
    component.name="postgres" \
    component.postgres.version="10.3"

USER ${POSTGRESQL_USER}:${POSTGRESQL_GROUP}

ENTRYPOINT ["/entrypoint.sh"]

CMD ["postgres"]
