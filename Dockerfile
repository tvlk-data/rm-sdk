FROM python:3

RUN apt-get update \
	&& pip install -U sphinx

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
