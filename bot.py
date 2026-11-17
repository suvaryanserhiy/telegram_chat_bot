from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes,
    MessageHandler, PollAnswerHandler, filters,
)
from modules import leveling_system
from modules.commands.exp_command import get_user_exp
from modules.commands.top_command import top
from modules.commands.daily_command import daily
from modules.commands.duel_command import duel, duel_answer
from modules.commands.quiz_command import quiz, quiz_answer
from dotenv import load_dotenv
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

COMMANDS = [
    ("exp", "Твій рівень і козацьке звання"),
    ("top", "Топ-10 козаків"),
    ("daily", "Щоденна пайка XP"),
    ("duel", "Дуель на XP (відповіддю на повідомлення)"),
    ("quiz", "Вікторина про Україну"),
    ("help", "Список команд"),
]

HELP_TEXT = (
    "Слава Україні! 🇺🇦\n"
    "Пиши в чат — отримуй XP і піднімайся від Джури до Гетьмана.\n"
    "Текст +1, стікер +2, фото +5, голосове −4 😉\n\n"
    + "\n".join(f"/{name} — {description}" for name, description in COMMANDS)
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await leveling_system.handle_message(update, context)


async def post_init(application):
    # Shows the commands in Telegram's "/" menu
    await application.bot.set_my_commands(COMMANDS)


# Build the bot
app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

# Handlers
app.add_handler(CommandHandler(["start", "help"], start))
app.add_handler(CommandHandler('exp', get_user_exp))
app.add_handler(CommandHandler('top', top))
app.add_handler(CommandHandler('daily', daily))
app.add_handler(CommandHandler('duel', duel))
app.add_handler(CallbackQueryHandler(duel_answer, pattern=r"^duel:"))
app.add_handler(CommandHandler('quiz', quiz))
app.add_handler(PollAnswerHandler(quiz_answer))
# New messages only: edits and channel posts have no XP-earning user
app.add_handler(MessageHandler(filters.UpdateType.MESSAGE & ~filters.COMMAND, on_message))


if __name__ == "__main__":
    app.run_polling()
