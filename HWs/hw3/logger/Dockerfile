FROM alpine:latest
  
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt install -y python3 python3-pip
RUN pip3 install paho-mqtt
COPY logger.py logger.py
COPY llogger.py llogger.py
CMD python3 logger.py
