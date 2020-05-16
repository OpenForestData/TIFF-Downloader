FROM python:3.8-alpine

WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add vips \
    vips-dev \
    build-base && \
    rm -rf /var/cache/apk/*

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]