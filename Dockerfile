FROM python:3.8-alpine AS build

COPY . /build
WORKDIR /build
RUN python3 setup.py install

ENTRYPOINT ["cosmos_exporter"]
