# Project's API Documentation

This directory contains documentation about developed source code modules.<br>
In order to build an *html* version of it, use available makefile.<br>
Then, you can open *_build/html/index.html* with the browser of your choice.

> [run_dev.sh](config/CONFIG.md#run-docker-container) conveniently maps the entire repository as a volume.

```bash
  pwd
  # <...>/DeepPantry

  # Launch a development container and attach to it.
  config/run_dev.sh
  sudo docker exec -it deep-pantry-dev /bin/bash
  cd /DeepPantry/
  pip3 install -r requirements.txt
  
  cd ./docs/
  make html

  # After you read documentation.
  exit
  sudo docker stop deep-pantry-dev
```