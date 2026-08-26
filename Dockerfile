FROM python:3.13-slim

WORKDIR /home/myapp

COPY requirements.txt .

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "setuptools>=83.0.0" "msgpack>=1.2.1"

COPY . .

EXPOSE 5050

CMD ["python", "sample_app.py"]