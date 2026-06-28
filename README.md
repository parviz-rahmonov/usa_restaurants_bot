# 🍽 USA Restaurants Bot

A Telegram bot for exploring restaurants across US states, built with Python 3.12 and aiogram 3.x.

---

## 📱 Features

**Public**
- `/start` — welcome screen with US state selection
- Browse restaurants by state via Inline buttons
- View restaurant details: name, phone, address, delivery status
- Links to Telegram channel or Google Maps
- Filter by 🚚 Delivery Only

**Admin** (`/admin`)
- ➕ Add Restaurant — step-by-step FSM form
- ✏️ Edit Restaurant — update any field
- 🗑 Delete Restaurant — with confirmation
- 📋 View Restaurants — full list by state
- Access restricted by Telegram ID

---

## 🛠 Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.12 |
| aiogram | 3.x |
| python-dotenv | 1.0+ |
| FSM Storage | Memory (MemoryStorage) |

---

## 📁 Project Structure

usa_restaurants_bot/

├── bot.py                  # Entry point

├── config.py               # Settings loader

├── constants.py            # All strings and callback data

│

├── data/

│   └── restaurants.py      # Restaurant data store

│

├── filters/

│   ├── admin.py            # IsAdminFilter

│   └── chat_type.py        # ChatTypeFilter

│

├── handlers/

│   ├── start.py            # /start command

│   ├── states_list.py      # State selection

│   ├── restaurants.py      # Delivery filter

│   └── admin/

│       ├── menu.py         # /admin command

│       ├── add.py          # Add FSM

│       ├── edit.py         # Edit FSM

│       ├── delete.py       # Delete FSM

│       └── view.py         # View list

│

├── keyboards/

│   ├── builder.py          # Base keyboard builder

│   ├── states_kb.py        # States keyboard

│   ├── restaurants_kb.py   # Restaurants keyboard

│   └── admin_kb.py         # Admin keyboards

│

├── states/

│   └── admin_states.py     # FSM state groups

│

└── utils/

└── formatters.py       # Text formatters

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/usa-restaurants-bot.git
cd usa-restaurants-bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
```

> Get a token from [@BotFather](https://t.me/BotFather).  
> Get your Telegram ID from [@userinfobot](https://t.me/userinfobot).

### 5. Run the bot

```bash
python bot.py
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Telegram bot token from @BotFather |
| `ADMIN_IDS` | ✅ | Comma-separated admin Telegram IDs |

---

## 🔐 Admin Access

Only users listed in `ADMIN_IDS` can use `/admin`.  
All others receive: `⛔ Access denied.`

---

## 📦 Data Storage

Restaurants are stored in a Python dictionary in `data/restaurants.py`.  
All changes made via the admin panel persist for the lifetime of the process.

> To add persistent storage, replace `data/restaurants.py` with a database repository layer.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push and open a Pull Request

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

