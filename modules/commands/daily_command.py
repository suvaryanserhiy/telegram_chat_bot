import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import ContextTypes
from modules import leveling_system

KYIV = ZoneInfo("Europe/Kyiv")
MAX_STREAK_BONUS_DAYS = 7


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = leveling_system.get_user(update.effective_user)
    today = datetime.now(KYIV).date()

    if user.last_daily == today.isoformat():
        await update.message.reply_text("🍞 Пайку на сьогодні вже видано. Приходь завтра!")
        return

    yesterday = (today - timedelta(days=1)).isoformat()
    user.streak = user.streak + 1 if user.last_daily == yesterday else 1
    user.last_daily = today.isoformat()

    amount = random.randint(5, 15) + min(user.streak, MAX_STREAK_BONUS_DAYS) * 2
    note = leveling_system.award(user, amount)
    leveling_system.save()

    text = f"🍞 {user.name} отримує щоденну пайку: +{amount} XP\n🔥 Серія: {user.streak} дн. поспіль"
    if note:
        text += f"\n{note}"
    await update.message.reply_text(text)
