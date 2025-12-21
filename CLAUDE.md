# Kimchi Premium Tracker

This project tracks the kimchi premium (price difference between Korean and international cryptocurrency exchanges).

## Features

* Runs every 5 minutes on GitHub Actions
* Computes current kimchi premium using BTC, ETH, and XRP prices
* Stores data in CSV format on gh-pages branch
* Visualizes data with a simple line chart on GitHub Pages
* Sends notifications via Telegram Bot and ntfy.sh when premium crosses 0.5% interval grids
* Grid-based notification system prevents spam (only notifies on grid crossings)
* Minimal dependencies: aiohttp, pydantic, python-dotenv

## Setup

### 1. Initial Setup

```bash
# Install dependencies
uv sync

# Run locally to test
uv run python main.py
```

### 2. Configure GitHub Repository

1. Go to repository Settings → Pages
2. Set Source to "gh-pages" branch
3. Save

### 3. Configure GitHub Secrets and Variables

**Secrets** (Settings → Secrets and variables → Actions → Secrets):
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather (keep secret!)

**Variables** (Settings → Secrets and variables → Actions → Variables):
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID (can be public)
- `NTFY_TOPIC`: Your ntfy.sh topic name (can be public, optional)

### 4. Push to GitHub

The workflow will automatically:
- Bootstrap the gh-pages branch on first run
- Run every 5 minutes to collect data
- Commit data to gh-pages branch

## Architecture

### Data Collection
- `main.py`: Main entry point
- `kimp/exchanges/`: Exchange API clients (Upbit, Binance, Naver)
- `kimp/types.py`: Data types

### Notification System
- `kimp/notification_manager.py`: Grid calculation and notification orchestration
- `kimp/notifiers/`: Notifier implementations (Telegram, Ntfy)
- Grid intervals: -1.0~-0.5 → -1.0, -0.5~0.0 → -0.5, 0.0~0.5 → 0.0, 0.5~1.0 → 0.5

### Data Storage
- CSV files stored in gh-pages branch
- Format: timestamp,usd_krw,est_usd_krw,premium
- One file per day: YYYY-MM-DD.csv
- Notification state tracked in .notification_state

### Visualization
- `pages/index.html`: Simple HTML page with Chart.js
- Displays last 7 days of data
- Updates automatically as new data is collected

## Expected Behavior

* Runs every 5 minutes via GitHub Actions
* Computes kimchi premium by comparing Korean (Upbit) and international (Binance) prices
* Saves data to gh-pages branch in CSV format
* Notifies via Telegram and ntfy when premium crosses 0.5% grid boundaries
* Only notifies once per grid crossing (no duplicate alerts)
* Minimal dependencies and simple codebase

