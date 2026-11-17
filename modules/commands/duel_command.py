import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from modules import leveling_system

DEFAULT_STAKE = 10
MAX_STAKE = 100


async def duel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/duel [stake], sent as a reply to the opponent's message."""
    reply = update.message.reply_to_message
    opponent = reply.from_user if reply else None
    if not opponent or opponent.is_bot or opponent.id == update.effective_user.id:
        await update.message.reply_text("⚔️ Відповідай командою /duel <ставка> на повідомлення суперника.")
        return

    try:
        stake = int(context.args[0]) if context.args else DEFAULT_STAKE
    except ValueError:
        stake = 0
    if not 1 <= stake <= MAX_STAKE:
        await update.message.reply_text(f"Ставка має бути числом від 1 до {MAX_STAKE} XP.")
        return

    challenger = leveling_system.get_user(update.effective_user)
    if challenger.total_xp < stake:
        await update.message.reply_text(f"У тебе лише {challenger.total_xp} XP — замало для такої ставки.")
        return

    data = f"{challenger.id}:{opponent.id}:{stake}"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⚔️ Прийняти", callback_data=f"duel:yes:{data}"),
        InlineKeyboardButton("🏳️ Відмовитись", callback_data=f"duel:no:{data}"),
    ]])
    await update.message.reply_text(
        f"⚔️ {challenger.name} викликає {opponent.first_name} на дуель! Ставка: {stake} XP",
        reply_markup=keyboard,
    )


async def duel_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    _, answer, challenger_id, opponent_id, stake = query.data.split(":")
    stake = int(stake)

    if query.from_user.id != int(opponent_id):
        await query.answer("Це не твоя дуель 🙂", show_alert=True)
        return
    await query.answer()

    # Guard against a double tap resolving the same duel twice
    finished = context.bot_data.setdefault("finished_duels", set())
    key = (query.message.chat.id, query.message.message_id)
    if key in finished:
        return
    finished.add(key)

    opponent = leveling_system.get_user(query.from_user)
    challenger = leveling_system.users.get(int(challenger_id))
    if answer == "no" or challenger is None:
        await query.edit_message_text(f"🏳️ {opponent.name} відмовляється від дуелі.")
        return

    # Both must be able to pay, otherwise the winner would gain XP that nobody lost
    if min(challenger.total_xp, opponent.total_xp) < stake:
        await query.edit_message_text("💸 Комусь із дуелянтів не вистачає XP. Дуель скасовано.")
        return

    winner, loser = random.sample([challenger, opponent], 2)
    notes = [leveling_system.award(loser, -stake), leveling_system.award(winner, stake)]
    leveling_system.save()

    lines = [f"🏆 {winner.name} перемагає {loser.name} і забирає {stake} XP!"]
    lines += [note for note in notes if note]
    await query.edit_message_text("\n".join(lines))
