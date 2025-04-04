# Development

```bash
npm run dev
```

# Deployment

## Building The Docker Image

```bash
docker build . -t api-playground/javascript:latest
```

## Running The Server

```bash
docker run --name api-playground-javascript -d --restart always -p 3000:3000 api-playground/javascript:latest
```


