FROM ubuntu:latest
  
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt install -y python3 python3-pip
RUN pip3 install paho-mqtt
COPY listener.py listener.py
CMD python3 listener.py
