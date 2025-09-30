FROM nginx:1.29.1-alpine

# To locally connect your container image to a repository:
LABEL org.opencontainers.image.source=https://github.com/SojusanApps/my-game-list-backend

RUN apk --no-cache add curl=8.14.1-r1 \
    && mkdir /etc/nginx/ssl \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
COPY proxy.conf /etc/nginx
