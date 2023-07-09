FROM ubuntu:bionic-20230308
RUN apt-get update && apt-get install wget -y
RUN wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && dpkg -i cloudflared-linux-amd64.deb

RUN ls

CMD ["/bin/sh"]