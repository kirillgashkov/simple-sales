FROM alpine:3.17


ENV MIGRATE_RELEASE_TAG=v4.15.2

RUN apk update \
 && apk add bash postgresql15-client curl \
 && curl -sSL "https://github.com/golang-migrate/migrate/releases/download/$MIGRATE_RELEASE_TAG/migrate.linux-amd64.tar.gz" | tar -xz -C /usr/local/bin migrate \
 && rm -rf /var/cache/apk/*


WORKDIR /app/

COPY ./ /app/

CMD ["bash"]
