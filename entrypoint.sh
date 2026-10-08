#!/bin/sh

set -e

if [ "${DB_ENGINE}" = "postgres" ]; then
  echo "[entrypoint] esperando a ${DB_HOST}:${DB_PORT}"
  until python -c "
import os, socket, sys
s = socket.socket()
s.settimeout(2)
try:
    s.connect((os.environ['DB_HOST'], int(os.environ['DB_PORT'])))
except Exception:
    sys.exit(1)
finally:
    s.close()
"; do
    sleep 2
  done
  echo "[entrypoint] base de datos disponible"
fi

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "[entrypoint] aplicando migraciones"
  python manage.py migrate --noinput
fi

exec "$@"