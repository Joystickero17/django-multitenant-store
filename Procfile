web: gunicorn --bind :8000 --workers 3 --threads 2 multistore.wsgi:application
websocket: daphne -b 0.0.0.0 -p 5000 multistore.asgi:application
celeryworker: celery --app multistore worker --concurrency 2