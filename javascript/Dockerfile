FROM node:20-alpine

WORKDIR /usr/src/app

COPY package.json package-lock.json app.js entrypoint.sh ./
COPY bin ./bin
COPY prisma ./prisma
COPY routes ./routes

RUN touch database.sqlite
RUN npm ci

EXPOSE 3000
ENTRYPOINT ["/usr/src/app/entrypoint.sh", "file:/usr/src/app/database.sqlite"]