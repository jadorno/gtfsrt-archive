FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY default.py ./
COPY compress.py ./

CMD [ "python", "-u", "./default.py"]
