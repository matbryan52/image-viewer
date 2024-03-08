# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder0

RUN apt-get update && apt-get install -y \
    python3-venv \
    python3-pip \
    git \
    nodejs

FROM builder0 as builder

RUN python3.11 -m venv /venv/
RUN /venv/bin/pip install -U pip
RUN /venv/bin/pip install --no-cache wheel && /venv/bin/pip install --no-cache panel rosettasciio git+https://github.com/LiberTEM/LiberTEM-panel-ui

FROM builder0

COPY --from=builder /venv/ /venv/

COPY . /code/
RUN venv/bin/pip install --no-cache /code/

ENV PYTHONUNBUFFERED 1

RUN mkdir /data

# image-viewer server
EXPOSE 9732

CMD ["/venv/bin/image-viewer", "--port", "9732"]

# docker build -t image-viewer .
# docker run -p 9732:9732 --mount type=bind,source="$(pwd)"/data,target=/data,readonly image-viewer