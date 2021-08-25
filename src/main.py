#!/usr/bin/python3

"""Performs main program functionality.

After loading settings from config/.env file, starts a
Telegram chatbot and uses AI to handle food inventory.

Author:
    Andrés Pérez
"""

from inventory_telebot import InventoryTelebot
from inventory_manager import InventoryManager
from dotenv import dotenv_values
from os.path import join, dirname, isfile
import logging
from typing import Dict, Optional

PATH2ENV: str = join(dirname(dirname(__file__)), "config", ".env")
"""Path to program settings file."""

PATH2LOG: str = join(dirname(dirname(__file__)), "log", "app.log")
"""Path to program log file."""


def main() -> None:
    """Performs main program functionality"""
    # Set up logging system, to notify several situations during execution.
    logging.basicConfig(level=logging.INFO,
                        filename=PATH2LOG,
                        filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Main program started")

    try:
        if isfile(PATH2ENV):
            config: Dict[str, Optional[str]] = dotenv_values(PATH2ENV)
        else:
            raise FileNotFoundError("Need a .env file under config folder.")

        manager = InventoryManager(str(config["AI_MODEL"]),
                                   str(config["CLASS_LABELS"]),
                                   str(config["INPUT_URI"]),
                                   float(config["SENSITIVITY"]))

        telebot = InventoryTelebot(str(config["BOT_TOKEN"]),
                                   int(config["CHAT_ID"]),
                                   manager)
        # Start interactive chatbot.
        telebot.run()
    except Exception as e:
        logging.critical(f"Exception caught by main: {e}", exc_info=True)
    
    logging.info("Main program finished")


if __name__ == "__main__":
    main()
