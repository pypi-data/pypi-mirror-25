FROM python:2.7
MAINTAINER Ashwin Vishnu Mohanan <avmo@kth.se>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY apt_requirements.txt /usr/src/app/
RUN apt-get update
RUN apt-get install -y --no-install-recommends $(grep -vE "^\s*#" apt_requirements.txt  | tr "\n" " ")
# RUN apt-get install -y --no-install-recommends python python-pip python-dev

RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -U -r requirements.txt
COPY requirements_extra.txt /usr/src/app/
RUN pip install --no-cache-dir -U -r requirements_extra.txt
COPY . /usr/src/app

RUN mkdir -p /root/.config/matplotlib \
	&&  echo 'backend      : agg' > /root/.config/matplotlib/matplotlibrc
