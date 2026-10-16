FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --gid 10001 incidentops \
    && useradd --uid 10001 --gid incidentops --no-create-home --shell /usr/sbin/nologin incidentops

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
