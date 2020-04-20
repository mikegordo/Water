FROM ubuntu:latest

RUN mkdir /server
ADD . /server

RUN apt-get update
RUN apt-get -y install python3.7 python3-pip
RUN pip3 install --no-cache-dir -r /server/requirements.pip

RUN adduser --disabled-password --gecos '' myuser
RUN chown -R myuser:myuser /server
RUN chmod +x /server/start_server.sh

ENV PYTHONPATH "${PYTHONPATH}:/server/"

WORKDIR /server

EXPOSE 80
