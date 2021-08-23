"""Telegram chatbot agent end users can interact with.

This module provides a Telegram chat interface which can
take advantage of `InventoryManager`'s capabilities.

Author:
    Andrés Pérez
"""

from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Dispatcher,
                          CallbackContext)
from telegram import Update
from inventory_manager import InventoryManager


class InventoryTelebot:
    """Telegram chatbot which can be used to interact with `InventoryManager`.

    Note:
        You can get a deeper understsanding about
        class settings format under `CONFIG.md`.

    Args:
        token: Bot token obtained by Telegram's BotFather.
        chat_id: Numeric if for a chat the bot will participate in.
        manager: `InventoryManager` instance to handle inventory in real-time.

    Example::

        >>> man = InventoryManager("../models/model.onnx", "../models/labels.txt", "/dev/video0")
        >>> bot = InventoryTelebot("MY_TOKEN", 123456789, man)
        >>> bot.run()

    See Also:
        https://core.telegram.org/bots#creating-a-new-bot
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
        """Starts bot's process.

        Note:
            This is a blocking method until one of these
            signals is received: SIGINT, SIGTERM, SIGABRT.
        """
        disp: Dispatcher = self._updater.dispatcher
        disp.add_handler(CommandHandler("start", self._start))
        disp.add_handler(CommandHandler("help", self._help))
        self._updater.start_polling()
        self._updater.idle()

    def _start(self, update: Update, _: CallbackContext) -> None:
        # Ignore incoming messages from other chats.
        if update.effective_chat.id != self._chat_id:
            return

        update.message.reply_text("Welcome to DeepPantryBot!")
        update.message.reply_text("Type /help to get more information.")

    def _help(self, update: Update, _: CallbackContext) -> None:
        # Ignore incoming messages from other chats.
        if update.effective_chat.id != self._chat_id:
            return

        update.message.reply_text("Avaliable commands:\n\n"
                                  "/start -> Welcome message\n"
                                  "/help  -> Help message\n")
