FROM python:3.10

RUN mkdir /link_recorder_app

WORKDIR /link_recorder_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate