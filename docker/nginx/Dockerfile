FROM nginx:1.24.0-alpine

# To locally connect your container image to a repository:
LABEL org.opencontainers.image.source https://github.com/Sojusan/my-game-list

RUN apk --no-cache add curl=7.88.1-r1 openssl=3.0.8-r4 \
    && mkdir /etc/nginx/ssl \
    && openssl req -x509 -sha256 -nodes -days 365 -subj "/C=PL/ST=ST/L=L/O=MyGameList/CN=MyGameList" -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx-key.key -out /etc/nginx/ssl/nginx-cert.crt \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY proxy.conf /etc/nginx
