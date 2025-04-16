## How to start:
### 1. Launch docker images
```bash
docker-compose up -d
```
### 2. Launch django project
```bash
gunicorn config.wsgi:application
```
or 
```bash
python manage.py runserver
```
### 3. Launch celery
```bash
celery -A config worker
```
### 4. Launch RabbitMQ consumer
```bash
 python -m product_events.consumer   
```

