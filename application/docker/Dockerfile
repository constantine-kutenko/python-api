FROM alpine:3.9

#
#
#

ENV APP_ADDRESS=0.0.0.0 \
    APP_PORT=5000

COPY ./app /app
COPY docker/entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN apk add --no-cache python3 netcat-openbsd && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /usr/lib/python*/ensurepip && \
    rm -r /root/.cache && \
    pip install -r requirements.txt && \
    chmod +x /entrypoint.sh

LABEL name="python-api" \
      description="The application is written in Python and  provides a simple REST API to communicate with PostgreSQL database." \
      maintainer="Constantine Kutenko <constantine.kutenko@gmail.com>" \
      os="Alpine Linux 3.9" \
      component.name="python-api" \
      component.python-api.version="1.0" \
      component.python.version="3.6"

EXPOSE 5000/tcp

USER nobody:nobody

ENTRYPOINT ["/entrypoint.sh"]

CMD [ "python", "app.py" ]
