FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y python3-dev && \
    apt-get install -y --no-install-recommends gcc && \
    pip install -r requirements.txt && \
    apt-get remove -y python3-dev && apt-get remove -y gcc && apt-get -y autoremove

CMD ["python", "-u", "web3main.py"]