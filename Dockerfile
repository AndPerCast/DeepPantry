# Build project's Docker image.

FROM dustynv/jetson-inference:r32.6.1

RUN apt update
RUN apt install -y python3-lxml

RUN mkdir -p /DeepPantry/
WORKDIR /DeepPantry/

COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./src/ ./src/
ENTRYPOINT [ "/DeepPantry/src/main.py" ]
