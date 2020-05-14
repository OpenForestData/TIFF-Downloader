FROM python:3.8-slim-buster

WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]