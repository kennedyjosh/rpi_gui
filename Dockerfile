FROM arm32v7/debian:buster

# add user qtuser
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# install necessary packages 
# thanks: https://www.reddit.com/r/docker/comments/bv31s2/has_anyone_managed_to_get_pip_pillow_installed/?utm_source=share&utm_medium=web2x&context=3
RUN apt-get update && apt-get install -y python3-pyqt5 python3-pip python3-dev zlib1g-dev libjpeg-dev gcc musl-dev liblcms2-dev git python3-pyqt5.qtsvg

# needed to adjust images
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install Pillow

RUN python3 -m pip install requests

ADD --chown=qtuser . /app

WORKDIR /app

RUN git clone https://github.com/ClimaCell-API/weather-code-icons.git weather_icons/

# show OS and OS version
RUN cat /etc/issue && cat /etc/debian_version

# show python version
RUN python3 -V

# show PIL version
RUN python3 -c "import PIL; print(f'PIL {PIL.__version__}')"