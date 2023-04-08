from telegram import Update
from telegram.ext import ContextTypes

from decorator.command_handler import command_handler
from decorator.registered import registered


def get_info(data: dict) -> str:
    return "\n".join(create_user_info(user) for user in data.values())


def create_user_info(user: dict) -> str:
    reports = "\n".join(create_report_info(report) for report in user.get("reports", []))
    return f"Имя: {user['name']}\n" \
           f"Специализация: {user['specialisation']}\n" \
           f"Репорты:\n" \
        + reports


def create_report_info(report: dict) -> str:
    return report["name"]


@registered()
@command_handler("data")
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_info(context.bot_data) if bool(context.bot_data) else "No Data")
