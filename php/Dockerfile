FROM serversideup/php:8.4-fpm-nginx

USER root

WORKDIR /var/www/html

COPY . .
COPY ./.env.example ./.env

RUN composer install --optimize-autoloader --no-interaction --prefer-dist

RUN rm -f database/database.sqlite && touch database/database.sqlite

RUN chown -R www-data:www-data /var/www/html

USER www-data

ENV AUTORUN_ENABLED=true