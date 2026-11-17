# Telegram Chat Bot

A feature-rich Telegram bot with a gamified leveling system that rewards users with experience points (XP) for participating in chat conversations. Built with Python and the `python-telegram-bot` library.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Bot](#running-the-bot)
  - [Running with Flask Server](#running-with-flask-server)
- [Commands](#commands)
- [Leveling System](#leveling-system)
  - [XP Rewards](#xp-rewards)
  - [Level Calculation](#level-calculation)
- [Project Structure](#project-structure)
- [Data Storage](#data-storage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🤖 **Telegram Bot Integration**: Seamless integration with Telegram using the official `python-telegram-bot` library
- 📊 **Leveling System**: Gamified experience system that tracks user activity and awards XP
- 💾 **Data Persistence**: User data is automatically saved to JSON files for persistence
- 🌐 **Web Server Support**: Flask server integration for hosting on platforms like Render
- 🎯 **Message Type Detection**: Different XP rewards based on message type (text, photos, stickers, voice)
- ⬆️ **Level Up Notifications**: Automatic notifications when users level up
- ⬇️ **Level Down System**: Users can lose levels if they receive negative XP

## Requirements

- Python 3.8 or higher
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))
- pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd telegram_chat_bot
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   
   Create a `.env` file in the root directory:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   ```

   To get a bot token:
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow the instructions
   - Copy the token provided

## Configuration

The bot uses a `config.json` file to manage enabled modules:

```json
{
  "modules_enabled": ["level_system"]
}
```

Currently supported modules:
- `level_system`: Enables the XP and leveling functionality

## Usage

### Running the Bot

**Option 1: Run the bot directly** (for local development):
```bash
python bot.py
```

**Option 2: Run with Flask server** (for production/deployment):
```bash
python server.py
```

The Flask server runs on port 10000 by default (or the `PORT` environment variable if set), making it suitable for deployment on platforms like Render, Heroku, or Railway.

### Running with Flask Server

When using `server.py`, the bot runs in a separate thread while Flask handles HTTP requests. This ensures the bot stays alive even on platforms that require a web server.

Set the `PORT` environment variable if deploying:
```bash
export PORT=10000  # On Windows: set PORT=10000
python server.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start`, `/help` | Welcome message and command list |
| `/exp` | Your XP, level, Cossack rank and XP needed for the next level |
| `/top` | Top 10 users by total XP |
| `/daily` | Daily bonus 5–15 XP, plus +2 XP per day of streak (up to 7 days, Kyiv time) |
| `/duel [stake]` | Reply to someone's message to challenge them; they accept or decline with a button, winner takes the stake (1–100 XP, default 10) |
| `/quiz` | Quiz about Ukraine (group chats only, every 2 min); first correct answer gets +10 XP |

Ranks by level: Джура (1), Козак (3), Десятник (5), Хорунжий (8), Осавул (12), Сотник (17), Полковник (23), Гетьман (30).

### Command Examples

**`/start`**:
```
Hello! I'm alive 🧠
```

**`/exp`**:
```
XP: 45, Рівень: 3, 15 XP до наступного рівня.
```

If a user hasn't sent any messages yet:
```
Старенький, ти ще не такий крутий, щоб мати рівень
```

## Leveling System

The bot tracks user activity and awards experience points (XP) based on the type of messages sent.

### XP Rewards

Different message types award different amounts of XP:

| Message Type | XP Reward |
|--------------|-----------|
| Text messages | +1 XP |
| Photos | +5 XP |
| Stickers | +2 XP |
| Voice messages | -4 XP |

### Level Calculation

- **Base XP Multiplier**: 10
- **Level Up Formula**: `XP Required = Current Level × 10`
- **Level Down**: Users can lose levels if their XP becomes negative
- **Minimum Level**: Level 1 (XP cannot go below 0 at level 1)

**Example**:
- Starting at Level 1, you need 10 XP to reach Level 2
- At Level 2, you need 20 XP to reach Level 3
- At Level 3, you need 30 XP to reach Level 4
- And so on...

When a user levels up, the bot automatically sends a congratulatory message:
```
🎉 [User Name] досягнув/ла [Level] рівня!
```

When a user levels down (due to negative XP):
```
⬇️ [User Name] впав/ла до [Level] рівня...
```

## Project Structure

```
telegram_chat_bot/
├── bot.py                      # Main bot application entry point
├── server.py                   # Flask server for deployment
├── user.py                     # User class with XP handling logic
├── config.json                 # Module configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── modules/
│   ├── __init__.py
│   ├── leveling_system.py      # Core leveling system logic
│   ├── data_manager.py         # Data persistence functions
│   └── commands/
│       └── exp_command.py      # /exp command handler
├── storage/
│   └── users.json              # User data storage (auto-generated)
└── utils/
    └── logger.py               # Logging configuration
```

### Key Files

- **`bot.py`**: Initializes the bot, sets up command and message handlers
- **`server.py`**: Wraps the bot with a Flask server for cloud deployment
- **`user.py`**: Defines the `User` class with XP and level management
- **`modules/leveling_system.py`**: Handles message processing and XP distribution
- **`modules/data_manager.py`**: Manages loading and saving user data from/to JSON
- **`modules/commands/exp_command.py`**: Implements the `/exp` command

## Data Storage

User data is stored in `storage/users.json` in the following format:

```json
{
  "123456789": {
    "id": 123456789,
    "name": "User Name",
    "exp": 45,
    "level": 3
  }
}
```

- Data is automatically loaded when the bot starts
- Data is saved after each message that affects XP
- The storage directory is created automatically if it doesn't exist
- All data is persisted locally in JSON format

## Development

### Adding New Commands

1. Create a command handler function in `modules/commands/`:
   ```python
   from telegram import Update
   from telegram.ext import ContextTypes
   
   async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text("Response message")
   ```

2. Import and register in `bot.py`:
   ```python
   from modules.commands.my_command import my_command
   app.add_handler(CommandHandler("mycommand", my_command))
   ```

### Adding New Message Types

Edit the `xp_table` dictionary in `modules/leveling_system.py`:

```python
xp_table = {
    'text': 1,
    'photo': 5,
    'sticker': 2,
    'voice': -4,
    'video': 6,  # Add new types here
    'animation': 3
}
```

### Extending the Leveling System

Modify `XP_BASE` in `user.py` to change the XP multiplier, or adjust the level calculation logic in the `User.exp_handler()` method.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE) (or your preferred license).

---

**Note**: Make sure to keep your `BOT_TOKEN` secure and never commit it to version control. Always use environment variables or a `.env` file (which should be listed in `.gitignore`).
