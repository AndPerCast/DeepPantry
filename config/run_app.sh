#!/bin/bash

# Utility script to execute main application inside a Docker container.
# Author: Andrés Pérez

PROGNAME="$(basename $0)"

# Issues given error message.
# Arguments:
# $1 -> Message error.
error_exit() {
  echo -e "Script ${PROGNAME}\nError: ${1:-"Unknown error"}" 1>&2
  echo -e "Try '${PROGNAME} --help' to get more information.\n" 1>&2
  exit 1
}

# Displays script's usage information.
usage() {
  cat << _EOF_
Utility script to execute main application inside a Docker container.

Usage:
  $PROGNAME [--help] [TAG]

Make sure to run this script from project's root directory.
There you can build the image, for instance:
  docker build . -t deep-pantry

You may pass its tag name as TAG argument for this script.
By default, TAG will be the latest one from Docker Hub.
_EOF_
}

# Starts project's main application inside a Docker container.
# Arguments:
# $1 -> Image tag to create a container from, latest one as default.
start_container() {
  REPO_ROOT=$(pwd)
  
  test "$(basename ${REPO_ROOT})" = "DeepPantry" || error_exit "You are not in project's root directory."
  test -d ${REPO_ROOT}/config || error_exit "config folder does not exist."
  test -d ${REPO_ROOT}/log || error_exit "log folder does not exist."
  test -d ${REPO_ROOT}/models || error_exit "models folder does not exist"
  
  
  # Add sudo priviledges if needed.
  docker run -it --runtime nvidia --rm --network host \
             --volume ${REPO_ROOT}/config:/DeepPantry/config \
             --volume ${REPO_ROOT}/log:/DeepPantry/log \
             --volume ${REPO_ROOT}/models:/DeepPantry/models \
             --volume /tmp/argus_socket:/tmp/argus_socket \
             --device /dev/video0 \
             ${1:-andpercast/deep-pantry:latest}
}

if [ "$1" = "--help" ]; then
  usage
  exit 0
fi

start_container $1
