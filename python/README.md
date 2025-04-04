# Development

```bash
JWT_SECRET=secret ./entrypoint.sh
```

# Deployment

## Building The Docker Image

```bash
docker build . -t api-playground/python:latest
```

## Running The Server

```bash
docker run --name api-playground-python -d --restart always -p 3000:3000 api-playground/python:latest
```