from telegram.ext import CommandHandler

from utils.bot import app


def command_handler(command):
    def decorator(func):
        return CommandHandler(command, func)
    return decorator
