from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from decorator.command_handler import command_handler
from decorator.conversation_handler import conversation_handler
from decorator.message_handler import message_handler
from decorator.registered import registered
from decorator.text_handler import text_handler

NAME: int
AGE: int
FORMAT: int
SEGMENT: int
QUESTION: int
IS_TRANSFER: int
TRANSFER_TARGET: int
AGE, FORMAT, SEGMENT, QUESTION, IS_TRANSFER, TRANSFER_TARGET, END = range(7)

ONLINE = "Онлайн"
OFFLINE = "Офлайн"
MOB = "Семья мобилизованного"
REF = "Беженец"
YES = "Да"
NO = "Нет"

AGE_KEYBOARD = ReplyKeyboardMarkup([[ONLINE, OFFLINE]], one_time_keyboard=True)
FORMAT_KEYBOARD = ReplyKeyboardMarkup([[MOB, REF]], one_time_keyboard=True)
QUESTION_KEYBOARD = ReplyKeyboardMarkup([[YES, NO]], one_time_keyboard=True)


async def finish(update: Update):
    await update.message.reply_text("Спасибо! Отчёт сохранён", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


@command_handler("create_report")
async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"] = context.bot_data[effective_telegram_id].get("reports", []) + [dict()]
    await update.message.reply_text("Имя")
    return AGE


@text_handler()
async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["name"] = update.message.text
    await update.message.reply_text("Возраст")
    return FORMAT


@text_handler(f"^\\d+$")
async def format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["age"] = update.message.text
    await update.message.reply_text("Очно или онлайн", reply_markup=AGE_KEYBOARD)
    return SEGMENT


@text_handler()
async def segment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["format"] = update.message.text
    await update.message.reply_text("Семья мобилизованного или беженцы", reply_markup=FORMAT_KEYBOARD)
    return QUESTION


@text_handler(f"^({MOB}|{REF})$")
async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["segment"] = update.message.text
    await update.message.reply_text("Кратко опишите суть запроса")
    return IS_TRANSFER


@text_handler()
async def is_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["question"] = update.message.text
    await update.message.reply_text("Был ли перевод к другому специалисту?", reply_markup=QUESTION_KEYBOARD)
    return TRANSFER_TARGET


@text_handler(f"^{YES}$")
async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["is_transfer"] = update.message.text
    await update.message.reply_text("К какому специалисту был перевод?")
    return END


@text_handler(f"^{NO}$")
async def no_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["is_transfer"] = update.message.text
    return await finish(update)


@text_handler()
async def transfer_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    context.bot_data[effective_telegram_id]["reports"][-1]["transfer_target"] = update.message.text
    return await finish(update)


@command_handler("cancel")
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_telegram_id = update.effective_user.id
    del context.bot_data[effective_telegram_id]["reports"][-1]
    await update.message.reply_text("Данные не сохранились", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


@message_handler()
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Некорректные данные")


@registered()
@conversation_handler()
def start_conversation():
    entry_points: list = [name]
    states: dict = {
        AGE: [age],
        FORMAT: [format],
        SEGMENT: [segment],
        QUESTION: [question],
        IS_TRANSFER: [is_transfer],
        TRANSFER_TARGET: [transfer, no_transfer],
        END: [transfer_target],
    }
    fallbacks: list = [cancel, fallback]

    return entry_points, states, fallbacks
