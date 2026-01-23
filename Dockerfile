FROM docker:24-dind

RUN apk add --no-cache curl bash kubectl helm nginx

RUN curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

COPY wiki_service /app/wiki_service
COPY wiki-chart /app/wiki-chart
COPY entrypoint.sh /entrypoint.sh
COPY setup-cluster.sh /setup-cluster.sh
COPY nginx.conf /etc/nginx/http.d/default.conf

RUN chmod +x /entrypoint.sh /setup-cluster.sh

WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
