# Development

```bash
npx prisma migrate deploy
npx prisma generate
npm run dev
```

# Deployment

## Building The Docker Image

```bash
docker build . -t api-playground/javascript:latest
```

## Running The Server

```bash
docker run --name api-playground-javascript -d -e DATABASE_URL="file:/usr/src/app/database.sqlite" --restart always -p 3000:3000 api-playground/javascript:latest
```


