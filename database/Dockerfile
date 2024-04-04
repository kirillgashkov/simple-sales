FROM alpine:3.17


ENV MIGRATE_RELEASE_TAG=v4.15.2
ENV WAIT_FOR_IT_COMMIT=81b1373f17855a4dc21156cfe1694c31d7d1792e

RUN apk update \
 && apk add bash postgresql15-client curl \
 && curl -sSL "https://github.com/golang-migrate/migrate/releases/download/$MIGRATE_RELEASE_TAG/migrate.linux-amd64.tar.gz" | tar -xz -C /usr/local/bin migrate \
 && curl -sSL https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_COMMIT}/wait-for-it.sh > /usr/local/bin/wait-for-it.sh && chmod +x /usr/local/bin/wait-for-it.sh \
 && rm -rf /var/cache/apk/*


WORKDIR /app/

COPY ./ /app/

ENTRYPOINT ["/app/docker-entrypoint.sh"]
