# CONTRIBUTING

## How to run the Dockerfile locally- app and redis

```
docker run -dp 80:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"

docker run -w /app IMAGE_NAME sh -c "rq worker -u rediss://token@singapore-redis.render.com:6379 emails"

```

## How to run the background worker in render.com

```
./bin/bash -c cd /some/dir && rq worker -c settings

```