# backend-fastapi-course

### создание одной docker сети
docker network create my_network

## запуск контейнеров
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network my_network \
    -v pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network my_network \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network my_network \
    booking_image

docker run --name booking_celery_worker \
    --network my_network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network my_network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking_nginx \
    -v ./nginx.conf:/etc/nginx/nginx.conf \
    --network my_network \
    --rm -p 80:80 nginx

### собираем docker-образ 
docker build -t booking_image . 
