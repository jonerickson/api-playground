FROM python:3.11-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY books ./books

RUN pipenv install --system --deploy

EXPOSE 3000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]