from telegram.ext import CommandHandler, MessageHandler, filters

from utils.bot import app


def text_handler(regex=None):
    def decorator(func):
        return MessageHandler((filters.TEXT if regex is None else filters.Regex(regex)) & ~filters.COMMAND, func)
    return decorator
