FROM kvendingoldo/diploma:base

ENV DISPLAY=:0.0 \
    MPLBACKEND="agg"

RUN mkdir -p /opt/diploma
WORKDIR /opt/diploma/fem

COPY ./python/requirements.txt /opt/diploma
COPY ./python/fem /opt/diploma
