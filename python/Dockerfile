FROM python:3.11-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock entrypoint.sh ./
COPY database ./database
COPY books ./books

RUN touch database.sqlite
RUN pipenv install --system --deploy

EXPOSE 3000
ENTRYPOINT ["/usr/src/app/entrypoint.sh", "/usr/src/app/database.sqlite"]