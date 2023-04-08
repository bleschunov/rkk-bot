from utils.bot import app


def registered():
    def decorator(handler):
        app.add_handler(handler)
        return handler

    return decorator