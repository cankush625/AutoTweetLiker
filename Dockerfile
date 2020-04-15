FROM python:3.7-alpine

ENV PYTHONONBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt