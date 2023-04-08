from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from decorator.conversation_handler import conversation_handler
from decorator.message_handler import message_handler
from decorator.registered import registered
from decorator.text_handler import text_handler
from decorator.command_handler import command_handler

SPECIALISATION: int
END: int
SPECIALISATION, END = range(2)


@command_handler("start")
async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id] = dict()
    await update.message.reply_text("Привет! Как вас зовут?")
    return SPECIALISATION


@text_handler()
async def specialisation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["name"] = update.message.text
    await update.message.reply_text("Какая у вас специализация?")
    return END


@text_handler()
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["specialisation"] = update.message.text
    await update.message.reply_text("Спасибо! Инструкция...")
    return ConversationHandler.END


@message_handler()
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите текст")


@registered()
@conversation_handler()
def start_conversation():
    entry_points: list = [name]
    states: dict = {
        SPECIALISATION: [specialisation],
        END: [end],
    }
    fallbacks: list = [fallback]

    return entry_points, states, fallbacks
