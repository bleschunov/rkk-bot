from telegram.ext import MessageHandler, filters

from utils.bot import app


def message_handler():
    def decorator(func):
        return MessageHandler(filters.ALL, func)
    return decorator
