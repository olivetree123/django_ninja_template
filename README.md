# django_ninja_template

A project tempalte for `django-ninja`

### Install requirements
```bash
poetry install
```

### Set environment variables
Edit file `.env`
```bash
DEBUG=True

# DATABASE, MYSQL OR POSTGRESQL
DB_ENGINE=django.db.backends.mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=django_ninja_template

# REDIS
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### Run
```bash
poetry run uvicorn django_ninja_template.asgi:application --host 0.0.0.0 --port 5000
```

### View api docs
```bash
https://localhost:5000/api/docs
```