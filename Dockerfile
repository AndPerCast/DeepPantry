# Build project's Docker image.

FROM dustynv/jetson-inference:r32.6.1

COPY requirements.txt /etc/
RUN pip3 install -r /etc/requirements.txt --no-cache-dir

# RUN mkdir -p /DeepPantry/
# WORKDIR /DeepPantry/
# COPY ./src/ ./src/
# CMD [ "/usr/bin/python3", "./src/main.py" ]
