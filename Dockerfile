FROM arm32v7/debian:buster

RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

RUN apt-get update && apt-get install -y python3-pyqt5 python3-pip zlib1g-dev libjpeg-dev gcc musl-dev

RUN pip3 install pillow

ADD . /app

COPY . /app

RUN chmod 777 app/img/*