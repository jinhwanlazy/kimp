# Kimchi Premium Tracker

> ⚠️ **Experimental Project**: This is a vibe-coding experiment built entirely by [Claude Code](https://claude.ai/claude-code), not a serious production system.

Real-time tracker for the "Kimchi Premium" - the price difference between Korean and international cryptocurrency exchanges.

## Features

- Tracks BTC, ETH, XRP prices across Upbit (KR) and Binance (INT)
- Runs every 5 minutes via GitHub Actions
- Stores data as CSV on gh-pages branch
- Live visualization at GitHub Pages
- Telegram & ntfy.sh notifications on 0.5% grid crossings

## Quick Start

```bash
# Install dependencies
uv sync

# Run locally
uv run python main.py
```

## Setup for GitHub Actions

See [CLAUDE.md](CLAUDE.md) for full setup instructions.

1. Enable GitHub Pages (Settings → Pages → gh-pages branch)
2. Add GitHub secrets/variables for notifications (optional)
3. Push to GitHub - workflow runs automatically and bootstraps everything

## About

This project was created as an experiment in "vibe-coding" - letting an AI assistant (Claude Code) implement a complete working system from a brief specification. The entire codebase, from API clients to notification system to visualization, was written by Claude.

It's functional but should be treated as a proof-of-concept rather than production-ready software.

## License

Unlicense (Public Domain)
