import random
import time

from telegram import Poll, Update
from telegram.ext import ContextTypes
from modules import leveling_system

QUIZ_XP = 10
QUIZ_SECONDS = 30
QUIZ_COOLDOWN = 120  # seconds between quizzes in one chat, so XP can't be farmed

# (question, correct answer, wrong answers...)
QUESTIONS = [
    ("У якому році Україна проголосила незалежність?", "1991", "1989", "1990", "1996"),
    ("Хто автор «Енеїди» — першого твору нової української літератури?", "Іван Котляревський", "Тарас Шевченко", "Іван Франко", "Григорій Сковорода"),
    ("Найвища гора України?", "Говерла", "Петрос", "Піп Іван", "Ай-Петрі"),
    ("Хто написав музику до гімну України?", "Михайло Вербицький", "Микола Лисенко", "Павло Чубинський", "Микола Леонтович"),
    ("Хто автор слів гімну України?", "Павло Чубинський", "Тарас Шевченко", "Іван Франко", "Олександр Олесь"),
    ("Хто створив відому на весь світ обробку «Щедрика»?", "Микола Леонтович", "Михайло Вербицький", "Кирило Стеценко", "Станіслав Людкевич"),
    ("Яке місто було столицею радянської України у 1919–1934 роках?", "Харків", "Київ", "Одеса", "Дніпро"),
    ("Справжнє ім'я Лесі Українки?", "Лариса Косач", "Ольга Кобилянська", "Марія Вілінська", "Олена Пчілка"),
    ("Хто автор «Лісової пісні»?", "Леся Українка", "Ліна Костенко", "Ольга Кобилянська", "Марко Вовчок"),
    ("Хто написав «Тіні забутих предків»?", "Михайло Коцюбинський", "Іван Франко", "Василь Стефаник", "Ольга Кобилянська"),
    ("Хто автор Конституції 1710 року?", "Пилип Орлик", "Іван Мазепа", "Богдан Хмельницький", "Петро Дорошенко"),
    ("Хто був першим Президентом України?", "Леонід Кравчук", "Леонід Кучма", "Віктор Ющенко", "Михайло Грушевський"),
    ("Скільки літер в українській абетці?", "33", "32", "31", "34"),
    ("Скільки областей в Україні?", "24", "25", "22", "27"),
    ("Яке море, крім Чорного, омиває Україну?", "Азовське", "Балтійське", "Каспійське", "Мармурове"),
    ("Який обласний центр розташований найзахідніше?", "Ужгород", "Львів", "Луцьк", "Чернівці"),
    ("У якому році культуру приготування українського борщу внесли до списку спадщини ЮНЕСКО?", "2022", "2019", "2020", "2023"),
    ("Що сконструював уродженець Києва Ігор Сікорський?", "Перший серійний гелікоптер", "Перший супутник", "Перший танк", "Перший підводний човен"),
]


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("🧠 Вікторина працює лише в групових чатах.")
        return

    wait = int(context.chat_data.get("quiz_at", 0) + QUIZ_COOLDOWN - time.time())
    if wait > 0:
        await update.message.reply_text(f"⏳ Наступна вікторина через {wait} с.")
        return
    context.chat_data["quiz_at"] = time.time()

    question, answer, *wrong = random.choice(QUESTIONS)
    options = [answer, *wrong]
    random.shuffle(options)
    correct = options.index(answer)

    message = await update.effective_chat.send_poll(
        f"🧠 {question} (перший правильний: +{QUIZ_XP} XP)",
        options,
        type=Poll.QUIZ,
        correct_option_id=correct,
        is_anonymous=False,
        open_period=QUIZ_SECONDS,
    )
    context.bot_data.setdefault("quizzes", {})[message.poll.id] = {
        "chat_id": update.effective_chat.id,
        "correct": correct,
    }


async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    quizzes = context.bot_data.get("quizzes", {})
    quiz_info = quizzes.get(answer.poll_id)
    if not quiz_info or answer.user is None or list(answer.option_ids) != [quiz_info["correct"]]:
        return
    del quizzes[answer.poll_id]  # only the first correct answer wins

    user = leveling_system.get_user(answer.user)
    note = leveling_system.award(user, QUIZ_XP)
    leveling_system.save()

    text = f"🧠 {user.name} відповів/ла першим/ою правильно: +{QUIZ_XP} XP!"
    if note:
        text += f"\n{note}"
    await context.bot.send_message(quiz_info["chat_id"], text)
