FROM python:3.8-slim-bullseye

WORKDIR /scripts

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY ./scripts .

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]