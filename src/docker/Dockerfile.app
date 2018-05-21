FROM kvendingoldo/diploma:base

ENV DISPLAY=:0.0 \
    MPLBACKEND="agg"

RUN mkdir -p /opt/diploma
WORKDIR /opt/diploma/fem

COPY ./python/fem /opt/diploma
COPY ./resources /opt/diploma/resources
