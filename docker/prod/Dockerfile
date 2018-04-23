FROM python:3.6-alpine

ENV APP_DIR="/app"
ENV PYTHONIOENCODING="UTF-8"

# Add new user to run the whole thing as non-root.
RUN addgroup -S app \
    && adduser -G app -h $APP_DIR -D app

RUN apk update \
    && apk add --no-cache \
       gcc \
       gettext \
       jpeg \
       jpeg-dev \
       libc-dev \
       libxml2-dev \
       libxslt-dev \
       linux-headers \
       make \
       musl-dev \
       pcre-dev \
       postgresql \
       postgresql-dev \
       tzdata \
       zlib-dev

RUN cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
   && echo "Europe/Paris" > /etc/timezone

RUN pip install pipenv

COPY --chown=app:app . $APP_DIR

COPY ./docker/prod/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY ./docker/prod/uwsgi.ini /
RUN chmod +x /uwsgi.ini

WORKDIR $APP_DIR

RUN pipenv install --system

ENTRYPOINT ["/entrypoint.sh"]
