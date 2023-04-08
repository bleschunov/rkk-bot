from telegram.ext import ConversationHandler


def conversation_handler():
    def decorator(func):
        args = func()
        return ConversationHandler(*args)
    return decorator
