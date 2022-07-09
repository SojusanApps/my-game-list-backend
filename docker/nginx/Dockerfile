FROM nginx:1.23.0-alpine

RUN apk add curl openssl --no-cache \
    && mkdir /etc/nginx/ssl \
    && openssl req -x509 -sha256 -nodes -days 365 -subj "/C=PL/ST=Kujawsko-Pomorskie/L=Toruń/O=MyGameList/CN=MyGameList" -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx-key.key -out /etc/nginx/ssl/nginx-cert.crt \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY proxy.conf /etc/nginx
