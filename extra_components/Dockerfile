FROM alpine

RUN apk --no-cache add wget git unzip

ENV HACS_VERSION 1.11.3

VOLUME /home

RUN rm -rf /data
RUN mkdir /data

RUN wget -O /tmp/hacs.zip https://github.com/hacs/integration/releases/download/$HACS_VERSION/hacs.zip && \
    unzip /tmp/hacs.zip -d /data/hacs

ENTRYPOINT cp -R /data/* /home/
