FROM python:3

RUN mkdir -p /opt/diploma
WORKDIR /opt/diploma/fem

ENV DISPLAY=:0.0 \
    MPLBACKEND="agg"

COPY ./python/requirements.txt /opt/diploma
COPY ./python/fem /opt/diploma
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /opt/diploma/requirements.txt
