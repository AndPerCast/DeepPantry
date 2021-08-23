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
from telegram import Update, ParseMode
from inventory_manager import (InventoryManager,
                               ProductType,
                               UnkownClassNameError,
                               InvalidConstraintError)
from typing import List


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
        disp.add_handler(CommandHandler("inventory", self._inventory))
        disp.add_handler(CommandHandler("list", self._list))
        disp.add_handler(CommandHandler("setmin", self._setmin))
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
                                  "/help -> Help message\n"
                                  "/inventory -> Returns all products\n"
                                  "/list -> Makes a shopping list\n"
                                  "/setmin \"PRODUCT\" UNITS -> UNITS\n"
                                  "units of PRODUCT should be available\n"
                                  "constantly. Do include \" characters\n")

    def _inventory(self, update: Update, _: CallbackContext) -> None:
        # Ignore incoming messages from other chats.
        if update.effective_chat.id != self._chat_id:
            return

        l = [str(product) for product in self._manager.inventory().values()]
        update.message.reply_text("\n\n".join(l))

    def _list(self, update: Update, _: CallbackContext) -> None:
        # Ignore incoming messages from other chats.
        if update.effective_chat.id != self._chat_id:
            return

        products: List[ProductType] = list(self._manager.inventory().values())
        shopping_list: List[str] = ["\t*Shopping list\n"]
        list_cost: float = 0.0

        # Format product data to make a MarkdownV2 list.
        for product in products:
            if product.demand > 0:
                shopping_list.append(f"- _{product.name} x {product.demand}")
                list_cost += product.total_cost

        if products:
            shopping_list.append(f"\nCost: {list_cost}{products[0].currency}\n")

        update.message.reply_text("\n".join(shopping_list),
                                  parse_mode=ParseMode.MARKDOWN_V2)
    
    def _setmin(self, update: Update, context: CallbackContext) -> None:
        # Ignore incoming messages from other chats.
        if update.effective_chat.id != self._chat_id:
            return

        if not context.args:
            update.message.reply_text("Invalid command syntax.")
            return
        
        product, units, *_ = context.args
        product = product.strip("\"").lower()
        units = int(units)

        try:
            # Update minimum units for product.
            self._manager.update_constraint(product, units)
        except UnkownClassNameError:
            update.message.reply_text("Invalid value for PRODUCT.")
            return
        except InvalidConstraintError:
            update.message.reply_text("Invalid value for UNITS.")
            return

        update.message.reply_text(f"Ok, you need at least {units} {product}.")
