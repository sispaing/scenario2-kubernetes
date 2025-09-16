FROM nginx:alpine
COPY ./nginx.conf /etc/nginx/nginx.conf.template
COPY . /usr/share/nginx/html
RUN apk add --no-cache curl

CMD ["/bin/sh", "-c", "envsubst '${BACKEND_HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]