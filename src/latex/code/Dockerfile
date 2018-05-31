FROM python:3

ENV DISPLAY=:0.0 \
    MPLBACKEND="agg"

RUN mkdir -p /opt/diploma
WORKDIR /opt/diploma/fem

COPY ./python/requirements.txt /opt/diploma
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /opt/diploma/requirements.txt

COPY ./fem /opt/diploma
COPY ./resources /opt/diploma/resources
