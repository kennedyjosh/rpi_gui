FROM arm32v7/debian:buster

RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# thanks: https://www.reddit.com/r/docker/comments/bv31s2/has_anyone_managed_to_get_pip_pillow_installed/?utm_source=share&utm_medium=web2x&context=3
RUN apt-get update && apt-get install -y python3-pyqt5 python3-pip zlib1g-dev libjpeg-dev gcc musl-dev

# needed to adjust images
RUN pip3 install pillow

ADD . /app

COPY . /app

# need permissions to write to img files if needed
RUN chmod 666 app/img/*