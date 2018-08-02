FROM python:3.6-alpine

ENV APP_DIR="/app"
ENV PYTHONIOENCODING="UTF-8"

# Add new user to run the whole thing as non-root.
RUN addgroup -S app \
    && adduser -G app -h $APP_DIR -D app

# mailcap contains /etc/mime.types.
RUN apk update \
    && apk add --no-cache \
      gcc \
      gettext \
      libc-dev \
      linux-headers \
      mailcap \
      make \
      musl-dev \
      pcre-dev \
      postgresql \
      postgresql-dev \
      tzdata

RUN cp /usr/share/zoneinfo/Europe/Paris /etc/localtime \
   && echo "Europe/Paris" > /etc/timezone

RUN pip install pipenv==2018.7.1

COPY --chown=app:app . $APP_DIR

COPY ./docker/prod/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY ./docker/prod/uwsgi.ini /
RUN chmod +x /uwsgi.ini

WORKDIR $APP_DIR

# https://docs.pipenv.org/advanced/#deploying-system-dependencies
RUN pipenv install --system --deploy

ENTRYPOINT ["/entrypoint.sh"]
