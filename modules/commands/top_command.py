from telegram import Update
from telegram.ext import ContextTypes
from modules import leveling_system

MEDALS = ["🥇", "🥈", "🥉"]


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ranking = sorted(leveling_system.users.values(), key=lambda u: u.total_xp, reverse=True)[:10]
    if not ranking:
        await update.message.reply_text("Поки що ніхто не заробив XP. Пишіть у чат! ✍️")
        return

    lines = []
    for place, user in enumerate(ranking):
        mark = MEDALS[place] if place < len(MEDALS) else f"{place + 1}."
        lines.append(f"{mark} {user.name} — {user.title}, рів. {user.level} ({user.total_xp} XP)")

    await update.message.reply_text("🏆 Топ козаків:\n" + "\n".join(lines))
