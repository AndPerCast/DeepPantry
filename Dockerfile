# Build project's Docker image.

FROM dustynv/jetson-inference:r32.6.1

RUN mkdir -p /DeepPantry/
WORKDIR /DeepPantry/

COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./src/ ./
CMD [ "/usr/bin/python3", "./src/main.py" ]
