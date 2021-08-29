# Project settings

This directory contains several tools to customize project's behaviour.

## Main program configuration
You can alter settings loaded by main program by creating a file called<br>
***.env*** on this directory. Here are available parameters:

> Following paths belong to a [Docker container](#run-docker-container) file system; that is,<br>
> project's root directory is located under */DeepPantry*

| Parameter      | Type    | Description                                     |
| :-----         | :-----: | :-----                                          |
| `AI_MODEL`     | `str`   | s |
| `CLASS_LABELS` | `str`   | s          |
| `SENSITIVITY`  | `float` | s                       |
| `INPUT_URI`    | `str`   | s          |
| `BOT_TOKEN`    | `str`   | s         |
| `CHAT_ID`      | `int`   | s         |

For instance:

```.env
  AI_MODEL="/DeepPantry/models/ssd-mobilenet.onnx"
  CLASS_LABELS="/DeepPantry/models/labels.txt"
  SENSITIVITY=0.5
  INPUT_URI="/dev/video0"
  BOT_TOKEN="my_telegram_bot_token"
  CHAT_ID=123456789
```

<br>

## Telegram Bot API

## Run docker container

