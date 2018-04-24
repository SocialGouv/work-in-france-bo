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

RUN pip install pipenv

COPY --chown=app:app . $APP_DIR

COPY ./docker/dev/entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR $APP_DIR

RUN pipenv install --dev --system

ENTRYPOINT ["/entrypoint.sh"]
