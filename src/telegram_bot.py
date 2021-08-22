"""Telegram chatbot agent end users can interact with.

This module provides a Telegram chat interface which can
take advantage of `InventoryManager`'s capabilities.

Author:
    Andrés Pérez
"""

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update
from inventory_manager import InventoryManager


class TelegramBot:
    """
    """

    def __init__(self,
                 token: str,
                 chat_id: int,
                 manager: InventoryManager) -> None:        
        self._token = token
        self._chat_id = chat_id
        self._manager = manager
        self._updater = Updater(token=self._token, use_context=True)


    def run(self) -> None:
        """
        """
        disp: Dispatcher = self._updater.dispatcher
        disp.add_handler(CommandHandler("start", self._start))
        self._updater.start_polling()
        self._updater.idle()

    def _start(self, update: Update, _: CallbackContext) -> None:
        update.message.reply_text("Welcome to DeepPantryBot!")
