"""
"""

from inventory_telebot import InventoryTelebot
from dotenv import dotenv_values
from os.path import join, dirname, isfile
from typing import Dict, Optional


def main() -> None:
    config: Dict[str, Optional[str]] = dotenv_values(join(dirname(dirname(__file__)), "config", ".env"))
    # bot = InventoryTelebot(config["BOT_TOKEN"], int(config["CHAT_ID"]))
    # bot.run()


if __name__ == "__main__":
    main()
