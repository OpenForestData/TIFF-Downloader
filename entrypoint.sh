#!/bin/bash

cd /app
cp example.env .env
gunicorn 'tiff_downloader.app:get_app()' -b :8000
