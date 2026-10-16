FROM python:3.12.15-alpine3.24

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup -g 10001 -S incidentops \
    && adduser -u 10001 -S -D -H -s /sbin/nologin -G incidentops incidentops

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --requirement requirements.txt

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
COPY docker-entrypoint.sh /usr/local/bin/incidentops-entrypoint

RUN chmod 0555 /usr/local/bin/incidentops-entrypoint \
    && chown -R incidentops:incidentops /app

USER 10001:10001

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/incidentops-entrypoint"]
