FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install python3.6 python3.6-venv python3.6-dev python3-pip timidity portaudio19-dev ffmpeg -y && \
    python3.6 -m ensurepip

EXPOSE 5000

COPY requirements.txt /build/requirements.txt

WORKDIR /build

RUN python3.6 -m pip install -r requirements.txt

COPY . /build

ENTRYPOINT [ "python3.6" ]

CMD [ "app/main.py" ]