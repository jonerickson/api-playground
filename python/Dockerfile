FROM python:3.11-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv 

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock app.py init_db.py entrypoint.sh ./

RUN touch database.sqlite
RUN pipenv install --system --deploy

EXPOSE 3000
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]