#!/bin/bash

# Utility script to launch a developer environment.
# Author: Andrés Pérez

# Add sudo priviledges if needed.
docker run -d --runtime nvidia -it --rm --network host \
           --volume ~/DeepPantry:/DeepPantry \
           --volume /tmp/argus_socket:/tmp/argus_socket \
           --device /dev/video0 \
           --name="deep-pantry-dev" \
           dustynv/jetson-inference:r32.6.1
