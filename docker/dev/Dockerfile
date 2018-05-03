FROM python:3.6-alpine

ENV APP_DIR="/app"
ENV PYTHONIOENCODING="UTF-8"
ENV PYTHONUNBUFFERED=1
ENV PYTHONWARNINGS="default"

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

RUN pip install pipenv==11.10.1

COPY --chown=app:app . $APP_DIR

COPY ./docker/dev/entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR $APP_DIR

# Create a real virtualenv in dev: this will make it possible to use the pipenv upgrade workflow etc.
# https://github.com/pypa/pipenv/issues/1490#issuecomment-369288621
RUN pipenv --python 3.6
RUN pipenv install --verbose
RUN pipenv install --dev --verbose

ENTRYPOINT ["/entrypoint.sh"]
