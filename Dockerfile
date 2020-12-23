FROM python:3.8-slim

WORKDIR /bot

COPY . .

RUN apt-get update \
    && apt-get upgrade gcc -y \
    && pip install --upgrade pip\
    && pip install -r requirements.txt

CMD ["python", "main.py"]