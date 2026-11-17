from telegram import Update
from telegram.ext import ContextTypes
from modules import leveling_system
from user import XP_BASE


async def get_user_exp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in leveling_system.users:
        await update.message.reply_text(
            'Старенький, ти ще не такий крутий, щоб мати рівень'
        )
        return

    user = leveling_system.users[user_id]
    xp_to_next = (user.level * XP_BASE) - user.exp
    await update.message.reply_text(
        f'🎖 {user.title}\nXP: {user.exp}, Рівень: {user.level}, {xp_to_next} XP до наступного рівня.'
    )
