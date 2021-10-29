FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN apt update && \
    apt upgrade -y && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
CMD gunicorn api_review.wsgi:application --bind 0.0.0.0:8000
