FROM python:3.6.8-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

COPY requirements.txt /code/
RUN pip install -r code/requirements.txt

COPY library /library
COPY deploy/container_settings /library/library/settings.py
COPY deploy/migrations /migrations

COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh
CMD ["/bin/sh", "/entrypoint.sh"]
