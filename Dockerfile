FROM python:3.6

COPY ./requirements.txt ./
COPY ./app.py ./
COPY ./config.py ./
COPY ./constants.py ./

RUN pip install --no-cache-dir -r requirements.txt
