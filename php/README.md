# Development

```bash
composer install
composer dev
```

# Deployment

## Building The Docker Image

```bash
docker build . -t api-playground/php:latest
```

## Running The Server

```bash
docker run --name api-playground-php -d --restart always -p 3000:8080 api-playground/php:latest
```