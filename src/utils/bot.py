import os

from telegram.ext import ApplicationBuilder, PicklePersistence

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

persistence = PicklePersistence("db.bin")
app = ApplicationBuilder().token(TELEGRAM_TOKEN).persistence(persistence).build()
