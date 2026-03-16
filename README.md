# Polymarket Skill for OpenClaw

Browse prediction markets, check odds, research events, compare markets, track your portfolio, and trade on [Polymarket](https://polymarket.com) directly from your AI agent.

## What it does

- **Browse markets** - trending, search, filter by category (politics, crypto, sports, tech, and more)
- **Check odds** - real-time Yes/No prices, volume, end dates
- **Market research** - AI-powered analysis combining odds with context about the event
- **Compare markets** - side-by-side odds for related markets with arbitrage detection
- **Portfolio dashboard** - view positions, P&L, balances, and open orders in one view
- **View order books** - see bid/ask depth for any market
- **Price history** - track how odds have moved over time
- **Trade** - place limit and market orders (buy/sell) with built-in safety confirmations and cost transparency
- **Manage positions** - view open orders, cancel trades, check balances

## Quick start

### Install the skill

```bash
# Via OpenClaw CLI
openclaw install mvanhorn/clawdbot-skill-polymarket

# Or clone directly from GitHub
git clone https://github.com/mvanhorn/clawdbot-skill-polymarket.git ~/.openclaw/skills/polymarket
```

### Browse markets (works immediately, no setup)

Just ask your agent:
- "What's trending on Polymarket?"
- "Search Polymarket for AI regulation"
- "What are the odds on the Fed cutting rates?"
- "Research the Bitcoin $150K market for me"
- "Compare the 2028 presidential candidates"

### Trade (requires Polymarket CLI + wallet)

1. Install the [Polymarket CLI](https://github.com/Polymarket/polymarket-cli):
   ```bash
   curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
   ```

2. Set up a wallet:
   ```
   polymarket wallet create
   polymarket approve set
   ```

3. Ask your agent:
   - "Buy 10 shares of YES on [market] at $0.45"
   - "Show me my portfolio dashboard"
   - "What are my open positions?"
   - "Cancel all my orders"

All trades require explicit confirmation before executing. No surprises.

## Safety

- Trades preview by default. Nothing executes without `--confirm`.
- This is real money (USDC on Polygon). The Polymarket CLI is experimental software.
- Your private key lives in `~/.config/polymarket/config.json`. Keep it safe.
- Check the order book before placing large orders in low-volume markets.

## How it works

| Feature | Backend | Auth needed |
|---------|---------|-------------|
| Browse, search, trending, categories | Gamma API (Python) | None |
| Market research, comparison | Gamma API (Python) | None |
| Order books, price history | Polymarket CLI | None |
| Portfolio dashboard | Polymarket CLI | Wallet |
| Trading, orders, positions | Polymarket CLI | Wallet |

Read-only features work without installing anything extra. Trading wraps the official [Polymarket CLI](https://github.com/Polymarket/polymarket-cli) (Rust).

## Version

v2.0.0 - Portfolio dashboard, market research mode, comparison mode, trending dashboard, cost/fee transparency, error recovery, expanded usage examples.

## License

MIT
