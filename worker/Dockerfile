FROM ubuntu:latest

RUN mkdir /worker
ADD . /worker

RUN apt-get update
RUN apt-get -y install python3.7 python3-pip
RUN pip3 install --no-cache-dir -r /worker/requirements.pip

RUN adduser --disabled-password --gecos '' myuser
RUN chown -R myuser:myuser /worker
RUN chmod +x /worker/start_worker.sh

ENV PYTHONPATH "${PYTHONPATH}:/worker/"

WORKDIR /worker

EXPOSE 5300
