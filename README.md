# 📈 Crypto & Stock Tracker Discord Bot

A powerful, modular Discord bot for tracking **crypto** and **stock** prices, built with:

- ✅ Slash commands (`/price`, `/compare`, `/watchlist`)
- ✅ Real-time data via [Alpha Vantage API](https://www.alphavantage.co/)
- ✅ MySQL integration with connection pooling
- ✅ Persistent user watchlists
- ✅ Clean embed-based UI

---

## ✨ Features

### 📊 Crypto & Stock Commands
- `/crypto price <symbol>` — View latest crypto price
- `/crypto compare <symbol1> <symbol2>` — Compare two crypto assets
- `/stock price <symbol>` — Get latest stock quote
- `/stock compare <symbol1> <symbol2>` — Compare stock performance

### 📁 Watchlist Commands
- `/watchlist add <symbol> <asset>` — Add crypto/stock to watchlist
- `/watchlist remove <symbol>` — Remove from watchlist
- `/watchlist view <asset>` — See your tracked assets
- `/watchlist clear <asset>` — Clear all items from your list

### 🔐 Database Support
- Uses MySQL for persistent storage
- Watchlists are tied to unique Discord user IDs
- Connection pooling for performance

---

## 🧠 HOW TO SETUP

### 1. Install Python
- Tested and recommended python version is **Python 3.11.8**.

Download links:

| Windows | Linux | Mac |
|:-----------|:------------:|------------:|
|[Windows installer (64-bit)](https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe) | [source tarball](https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tgz) | [macOS 64‑bit universal2 installer](https://www.python.org/ftp/python/3.11.8/python-3.11.8-macos11.pkg) |
|[Windows installer (32‑bit)](https://www.python.org/ftp/python/3.11.8/python-3.11.8.exe) | | |
| [Windows installer (ARM64)](https://www.python.org/ftp/python/3.11.8/python-3.11.8-arm64.exe) | | |

### 2. 📥 Clone the repository
```bash
git clone https://github.com/yourusername/crypto-stock-tracker-bot.git
cd crypto-stock-tracker-bot
```

### 3. 🧪 Install dependencies

```bash
pip install -r requirements.txt
```
### 4. 🔑 Get your Alpha Vantage API Key
- Go to: https://www.alphavantage.co/support/#api-key

    - Sign up with your email to receive a free API key

    - Important: The free tier is limited to 25 requests per day

        - If you need more (e.g., for a public bot or frequent use), you’ll need to upgrade to Alpha Vantage Premium

### 5. 🔑 Get your Discord Bot Token

- Go to [discord developer portal](https://discord.com/developers/applications) and create a new application.
- Open your new application and go to the "Bot" tab.
- Click on Reset Token and copy the Token from there.

**Note: Do not share your Discord Bot Token with anyone who you do not trust.**

### 6. 📕 Database requirement.
**You need a __MySQL__ database to run this bot**, database is used to save user's data.


### 7. 📃 Configure your bot in config.yml
**If you do not see the config.yml file**, simply **start the bot by running main.py file** and it will automatically create a config.yml file.


**Default config file:**
 ```yaml
 # Your discord bot token - get it by creating an application at https://discord.com/developers/applications
TOKEN: ''

# Prefix is for the discord bot prefixed commands (such as !help, '!' is the prefix here)
PREFIX: '!'

# Alpha Vantage API key - get it from https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY: ''

# MySQL server host (e.g., localhost or IP address)
MYSQL_HOST: localhost

# MySQL server port (integer)
MYSQL_PORT: 3306

# MySQL username
MYSQL_USER: ''

# MySQL password (leave empty if no password is set)
MYSQL_PASSWORD: ''

# MySQL database name
MYSQL_DATABASE: ''
```

### 8. ▶️ Starting the bot

- **Run `main.py` file. **It will verify all the dependencies and start the bot.****

- If you see `Bot is online (<Your bot username>)`, it means its successfully started.
- If you see any error in `logs > latest.logs` or if the bot is not starting, report them by creating an issue in this repo.
