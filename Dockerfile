#BUILD Backend App Image
FROM php:8.0.7-fpm-alpine3.13

WORKDIR /var/www/html

#Essentials
RUN echo "UTC" > /etc/timezone
RUN apk add --no-cache zip unzip curl supervisor

#installing bash
RUN apk add bash
# RUN sed -i 's/bin\/ash/bin/bash/g' /etc/passwd

#Installing PHP module extension needed by Lumen Framework
# RUN apk add --no-cache php8-openssl \
#     # php8-pdo \
#     php8-mbstring

#Installing other PHP module extension
# RUN apk add --no-cache php8-cli \
#     php8-common \
#     # php8-pdo_mysql \
#     php8-fpm \
#     php8-json \
#     php8-tokenizer

#Create symbolic link. change the binary name because it's more common to use just php as a command than php8
# RUN ln -s /usr/bin/php8 /usr/bin/php
RUN docker-php-ext-install pdo_mysql
# RUN docker-php-ext-enable pdo pdo_mysql mbstring

#installing composer
RUN curl -sS https://getcomposer.org/installer -o composer-setup.php
RUN php composer-setup.php --install-dir=/usr/local/bin --filename=composer
RUN rm -rf composer-setup.php

#Build proccess
COPY . .
RUN rm -rf vendor
# RUN rm -rf public
# ADD ./public ./html
# RUN useradd jrs6200
RUN composer install --no-dev
RUN chown -R nobody:nobody /var/www/html/storage
RUN chmod -R o+w /var/www/html/storage
RUN chmod -R o+w /var/www/html/bootstrap
# RUN php -S localhost:9000 -t public

#Open Port to access apps
EXPOSE 9000
# CMD [ "php -S localhost:9000 -t public" ]
