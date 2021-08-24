#!/bin/bash

# Utility script to launch a container from project's image.

# Add sudo priviledges if needed.
docker run -d --runtime nvidia -it --rm --network host \
           --volume ../config:/DeepPantry/config \
           --volume ../log:/DeepPantry/log \
           --volume ../models:/DeepPantry/models \
           --volume /tmp/argus_socket:/tmp/argus_socket \
           --device /dev/video0 \
           deep-pantry
