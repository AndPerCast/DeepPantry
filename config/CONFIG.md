# Project settings

This directory contains several tools to customize project's behaviour.

## Main program configuration
You can alter settings loaded by main program by creating a file called<br>
***.env*** on this directory. Here are available parameters:

> Following paths belong to a [Docker container](#run-docker-container) file system; that is,<br>
> project's root directory is located under */DeepPantry*

| Parameter      | Type    | Description |
| :-----         | :-----: | :----- |
| `AI_MODEL`     | `str`   | Path to an [ONNX](https://onnx.ai) file that contains a machine learning model |
| `CLASS_LABELS` | `str`   | Path to a file that contains class labels to be recognized |
| `SENSITIVITY`  | `float` | Minimum confidence [0, 1] for an object to be detected |
| `INPUT_URI`    | `str`   | [Resource id](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-streaming.md#input-streams) for an image/camera input |
| `BOT_TOKEN`    | `str`   | [Bot](#telegram-bot-api) token obtained by Telegram's BotFather |
| `CHAT_ID`      | `int`   | Numeric id for a chat the [bot](#telegram-bot-api) will participate in |

For instance:

```.env
  AI_MODEL="/DeepPantry/models/ssd-mobilenet.onnx"
  CLASS_LABELS="/DeepPantry/models/labels.txt"
  SENSITIVITY=0.5
  INPUT_URI="/dev/video0"
  BOT_TOKEN="my_telegram_bot_token"
  CHAT_ID=123456789
```

If you prefer to use **MIPI CSI** (**port 0**) instead of USB camera:

```.env
  INPUT_URI="csi://0"
```

<br>

## Telegram Bot API

In order to interact with the application and get results, you must<br>
create a [Telegram](https://telegram.org/?setln=en) account first, via either mobile app, desktop app<br>
or browser.

After that, it's time to create a new [bot](https://core.telegram.org/bots#) by chating with **[BotFather](https://core.telegram.org/bots#6-botfather)**.<br>
Follow *[Creating a new bot](https://core.telegram.org/bots#creating-a-new-bot)* tutorial.

> Keep your token secure and store it safely, it can be used by<br>
> anyone to control your bot.

Start a chat session with your new bot, by typing its name in the<br>
search bar and send any message to it.

At this point there are two main alternatives to get the chat id:

> Replace *\<YourToken\>* with the one you got from previous step.

- Install ***python-telegram-bot*** library and execute this code,<br>
  you can do that inside the [development container](#run-docker-container):
```python
  >>> import telegram
  >>> bot = telegram.Bot(token='<YourToken>')
  >>> print(bot.get_me())
  >>> updates = bot.get_updates()
  >>> print(updates[0]['message']['chat']['id'])
  123456789
```

- Make this *HTTP* request on your browser and look for ***"id"***<br>
  field on *json* response:
```http
  https://api.telegram.org/bot<YourToken>/getUpdates
```

<br>

## Run Docker container

There are two utility scripts in this directory.

On the hand, ***run_app.sh*** is mainly designed to execute main<br>
application inside a Docker container, you can pass both local<br>
or [Docker Hub](https://hub.docker.com/r/andpercast/deep-pantry) image tag to run it from, though latest one will be<br>
pulled by default.

Several volumes will be mapped inside the new container:
- *DeepPantry/config*
- *DeepPantry/log*
- *DeepPantry/models*
- Video device files (*video0* and *argus_socket*)

> Make sure that you have set up a proper *[.env](#main-program-configuration)* file.

```bash
  pwd
  # <...>/DeepPantry

  # If you choose to build a local image.
  docker build . -t deep-pantry
  config/run_app.sh deep-pantry

  # Else, make sure to specify a proper image tag.
  config/run_app.sh andpercast/deep-pantry:latest

  # Get more information.
  config/run_app.sh --help
```