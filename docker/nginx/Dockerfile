FROM nginx:1.27.2-alpine

# To locally connect your container image to a repository:
LABEL org.opencontainers.image.source https://github.com/SojusanApps/my-game-list-backend

RUN apk --no-cache add curl=8.10.1-r0 openssl=3.3.2-r1 \
    && mkdir /etc/nginx/ssl \
    && openssl req -x509 -sha256 -nodes -days 365 -subj "/C=PL/ST=ST/L=L/O=MyGameList/CN=MyGameList" -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx-key.key -out /etc/nginx/ssl/nginx-cert.crt \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY proxy.conf /etc/nginx
