# Stellar System V3

A professional, feature-rich Discord bot for the **Stellar Universe** server, built with discord.py 2.x, full slash command support, a modular Cog architecture, and SQLite persistence.

---

## Features

| Category | Commands / Features |
|---|---|
| Owner | `/owner` — social media links |
| Rules | `/rules` — server rules embed |
| Welcome | `/setwelcome` — configurable welcome channel |
| Auto Role | `/setautorole`, `/remautorole`, `/viewautorole` |
| Tickets | `/ticketpanel`, `/close`, `/transcript`, `/delete` |
| Moderation | `/kick`, `/ban`, `/unban`, `/timeout`, `/untimeout`, `/purge`, `/warn`, `/warnings`, `/removewarn` |
| Logging | `/setlog`, `/viewlog` + automatic event logs |
| Server Info | `/serverinfo`, `/userinfo`, `/avatar`, `/roleinfo` |
| Utility | `/ping`, `/uptime`, `/botinfo`, `/help` |

---

## Requirements

- Python 3.13+
- A Discord bot token with the following **Privileged Gateway Intents** enabled:
  - **Server Members Intent** — for welcome, auto-role, and logging
  - **Message Content Intent** — for purge and transcript features

---

## Installation

### 1. Clone / download the project

```bash
git clone https://github.com/yourname/stellar-system-v2.git
cd stellar-system-v2
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here
STAFF_ROLE_ID=your_staff_role_id_here   # optional — for ticket permissions
OWNER_ID=your_discord_user_id_here      # optional — for owner-only checks
```

### 5. Enable Privileged Intents

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Select your bot → **Bot** tab
3. Enable **Server Members Intent** and **Message Content Intent**
4. Save changes

### 6. Invite the bot

Generate an OAuth2 URL with the `bot` and `applications.commands` scopes and the following permissions:

- Manage Roles
- Manage Channels
- Kick Members
- Ban Members
- Moderate Members (timeout)
- Read Messages / View Channels
- Send Messages
- Manage Messages
- Embed Links
- Attach Files
- Read Message History

---

## Running Locally

```bash
python main.py
```

On successful startup you will see:

```
Stellar System V2 successfully connected
Logged in as : StellarBot#0000 (123456789)
```

---

## Running on Railway

1. Create a new project on [railway.app](https://railway.app)
2. Connect your GitHub repository (or use Railway CLI to deploy)
3. Add environment variables in **Variables**:
   - `TOKEN`
   - `GUILD_ID`
   - `STAFF_ROLE_ID` *(optional)*
   - `OWNER_ID` *(optional)*
4. Set the **Start Command**:
   ```
   python main.py
   ```
5. Deploy — Railway will install dependencies from `requirements.txt` automatically

> **Note:** SQLite data is stored at `data/stellar.db`. On Railway, this is ephemeral. For persistent storage on Railway, mount a volume or migrate to PostgreSQL.

---

## Running on Koyeb

1. Create a new Koyeb app and connect your GitHub repository
2. In **Build settings**, ensure Python is detected
3. Set the **Run command**:
   ```
   python main.py
   ```
4. Add environment variables under **Environment**:
   - `TOKEN`, `GUILD_ID`, `STAFF_ROLE_ID`, `OWNER_ID`
5. Deploy the service

---

## Running on Replit

1. Import the project into a Replit Python repl
2. In the **Secrets** tab, add:
   - `TOKEN`, `GUILD_ID`, `STAFF_ROLE_ID`, `OWNER_ID`
3. In `.replit`, set:
   ```toml
   [run]
   command = "python main.py"
   ```
4. Click **Run**

> Use **UptimeRobot** or a similar pinger to keep the Replit repl alive 24/7 on the free tier.

---

## Running on Render

1. Create a new **Background Worker** service on [render.com](https://render.com)
2. Connect your GitHub repository
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
4. Add environment variables in **Environment**:
   - `TOKEN`, `GUILD_ID`, `STAFF_ROLE_ID`, `OWNER_ID`
5. Deploy

---

## Running on a VPS (Ubuntu / Debian)

```bash
# Install Python 3.13
sudo apt update && sudo apt install python3.13 python3.13-venv -y

# Clone and set up
git clone https://github.com/yourname/stellar-system-v2.git
cd stellar-system-v2
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # fill in your values

# Run with systemd (recommended for 24/7)
sudo nano /etc/systemd/system/stellar-bot.service
```

Paste:
```ini
[Unit]
Description=Stellar System V2 Discord Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/stellar-system-v2
ExecStart=/path/to/stellar-system-v2/.venv/bin/python main.py
Restart=always
RestartSec=5
EnvironmentFile=/path/to/stellar-system-v2/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable stellar-bot
sudo systemctl start stellar-bot
sudo systemctl status stellar-bot
```

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `TOKEN` | ✅ | Discord bot token |
| `GUILD_ID` | ✅ | Your main server (guild) ID |
| `STAFF_ROLE_ID` | ❌ | Role ID granted access to ticket channels |
| `OWNER_ID` | ❌ | Your Discord user ID for owner-only commands |

---

## Project Structure

```
stellar-system-v2/
├── main.py                  # Entry point — bot init, cog loading, startup checks
├── requirements.txt
├── .env.example
├── README.md
│
├── database/
│   ├── database.py          # Async SQLite interface (aiosqlite)
│   └── schema.sql           # SQL schema — applied on every startup (idempotent)
│
├── cogs/                    # Feature modules (one Cog per feature)
│   ├── owner.py
│   ├── rules.py
│   ├── welcome.py
│   ├── autorole.py
│   ├── tickets.py
│   ├── moderation.py
│   ├── logging_system.py
│   ├── utility.py
│   └── serverinfo.py
│
├── utils/
│   ├── embeds.py            # Embed factory functions
│   ├── checks.py            # Custom permission check decorators
│   ├── logger.py            # Rotating file + console logger
│   └── config.py            # Environment variable loading & validation
│
├── views/
│   ├── ticket_view.py       # Persistent ticket panel and action buttons
│   └── role_view.py         # Self-assignable role button panels
│
├── data/
│   └── stellar.db           # SQLite database (auto-created)
│
└── logs/
    └── bot.log              # Rotating log file (auto-created)
```

---

## License

MIT — free to use, modify, and distribute.
