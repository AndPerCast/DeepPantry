#!/bin/bash

# Utility script to launch a container from project's image.
# Make sure to run this script from project's root directory.
# There you can build the image, for instance:
#   docker build . -t deep-pantry

REPO_ROOT=$(pwd)

# Add sudo priviledges if needed.
docker run -it --runtime nvidia --rm --network host \
           --volume ${REPO_ROOT}/config:/DeepPantry/config \
           --volume ${REPO_ROOT}/log:/DeepPantry/log \
           --volume ${REPO_ROOT}/models:/DeepPantry/models \
           --volume /tmp/argus_socket:/tmp/argus_socket \
           --device /dev/video0 \
           deep-pantry
