FROM python:3.8-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends p7zip-full\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./main.py

CMD [ "python", "-u", "./main.py"]
