#

FROM dustynv/jetson-inference:r32.6.1

COPY requirements.txt /etc/
RUN pip3 install -r /etc/requirements.txt

# RUN mkdir -p /DeepPantry/
# WORKDIR /DeepPantry/
# COPY ./src/ ./src/
# ENTRYPOINT [ "/usr/bin/python3", "/DeepPantry/src/main.py" ]
