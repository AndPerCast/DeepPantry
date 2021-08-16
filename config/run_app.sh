#!/bin/bash

# Utility script to execute main app, inside a container.

sudo docker run --runtime nvidia -it --rm --network host \
                --volume ~/DeepPantry:/DeepPantry \
                --volume /tmp/argus_socket:/tmp/argus_socket \
                --device /dev/video0 \
                dustynv/jetson-inference:r32.6.1
