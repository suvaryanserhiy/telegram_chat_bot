from user import User
from modules.data_manager import save_data, load_data

users = {}

xp_table = {
    'text': 1,
    'photo': 5,
    'sticker': 2,
    'voice': -4
}

# Load existing users (older saves lack the newer fields, User() defaults cover them)
for uid, info in load_data().items():
    users[int(uid)] = User(int(uid), info["name"])
    vars(users[int(uid)]).update(info)


def get_user(tg_user):
    """Return the stored User for a Telegram user, creating it if needed."""
    if tg_user.id not in users:
        users[tg_user.id] = User(tg_user.id, tg_user.first_name)
    user = users[tg_user.id]
    user.name = tg_user.first_name  # keep up with name changes
    return user


def save():
    save_data({uid: vars(u) for uid, u in users.items()})


def award(user, amount):
    """Apply an XP change. Returns a level-change announcement, or None."""
    old_title = user.title
    result = user.exp_handler(amount)
    if result == "level_up":
        promotion = f" Нове звання: {user.title}!" if user.title != old_title else ""
        return f"🎉 {user.name} досягнув/ла {user.level} рівня!{promotion}"
    if result == "level_down":
        return f"⬇️ {user.name} впав/ла до {user.level} рівня..."
    return None


async def handle_message(update, context):
    user = get_user(update.effective_user)

    # Detect message type and assign XP
    exp_gain = next(
        (xp for attr, xp in xp_table.items() if getattr(update.message, attr, None)),
        0
    )

    note = award(user, exp_gain)
    save()

    if note:
        await update.message.reply_text(note)
