# DeepPantry
Let AI keep track of your food inventory and handle the shopping list for you

## Author

- [@AndPerCast](https://github.com/AndPerCast)

## License

[MIT](https://choosealicense.com/licenses/mit/)

<br>

## Overview


<br>

## Requirements


<br>

## Installation guide

First of all, you have to complete the [initial set up](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) of your Jetson Nano, which<br>
includes flashing the OS image on your SD card.

> This project has been tested under **JetPack 4.6.1**

Once you boot up, update your system and proceed to clone this repository,<br>
using following commands:

```bash
  sudo apt update
  sudo apt upgrade
  git clone https://github.com/AndPerCast/DeepPantry.git
```

It's time to configure the project:
- [Application settings](#settings)
- [AI models](#ai-models)

The best way to run the project is via a **Docker container**. There is a simple<br>
*Dockerfile* located on **project's root directory**, which you can further<br>
customize if you plan to enhance this application.

You can either build a local image or pull it from [Docker Hub](https://hub.docker.com/r/andpercast/deep-pantry).<br>
There is a script called [run_app.sh](config/CONFIG.md#run-docker-container) to execute main application inside a<br>
container. For example:

> You need to exert sudo priviledges if you are not a member of [docker group](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

```bash
  pwd
  # <...>/DeepPantry

  # If you choose to build a local image.
  docker build . -t deep-pantry
  config/run_app.sh deep-pantry

  # Else, make sure to specify a proper image tag.
  config/run_app.sh andpercast/deep-pantry:latest
```

<br>

## API documentation

You can find more information about API documentation [here](docs/DOCS.md).

<br>

## Settings

You can find more information about project settings [here](config/CONFIG.md).

<br>

## AI models

You can find more information about supported AI models [here](models/MODELS.md).

<br>

## Testing

You can find more information about project testing [here](tests/TESTS.md).