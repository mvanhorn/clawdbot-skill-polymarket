# Polymarket Skill for OpenClaw

Browse prediction markets, check odds, research events, compare markets, track your portfolio, and trade on [Polymarket](https://polymarket.com) directly from your AI agent.

## What it does

- **Browse markets** - trending, search, filter by category (politics, crypto, sports, tech, and more)
- **Check odds** - real-time Yes/No prices, volume, end dates
- **Market research** - AI-powered analysis combining odds with context about the event
- **Compare markets** - side-by-side odds for related markets with arbitrage detection
- **Portfolio dashboard** - view positions, P&L, balances, activity history, and open orders
- **View order books** - see bid/ask depth and spread for any market
- **Price history** - track how odds have moved over time (1m to max intervals)
- **Trade** - place limit, market, post-only, and batch orders with built-in safety confirmations
- **Leaderboard & analytics** - trader rankings, open interest, volume, top holders
- **Live streaming** - real-time comments and crypto prices via RTDS WebSocket
- **Bridge funds** - deposit and withdraw across EVM, Solana, and Bitcoin chains
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
- "Who are the top Polymarket traders?"

### Trade (requires Polymarket CLI + wallet)

1. Install the [Polymarket CLI](https://github.com/Polymarket/polymarket-cli) (Rust binary):
   ```bash
   brew install polymarket/tap/polymarket-cli
   ```

2. Set up a wallet:
   ```bash
   polymarket wallet create
   polymarket approve set
   ```

3. Use the interactive REPL for exploratory sessions:
   ```bash
   polymarket shell
   ```

4. Ask your agent:
   - "Buy 10 shares of YES on [market] at $0.45"
   - "Show me my portfolio dashboard"
   - "What are my open positions?"
   - "Cancel all my orders"
   - "Deposit funds from Ethereum"

All trades require explicit confirmation before executing. No surprises.

## APIs covered

This skill covers all 4 Polymarket APIs plus the Gamma convenience layer:

| API | Base URL | Purpose | Auth |
|-----|----------|---------|------|
| Gamma | gamma-api.polymarket.com | Browse, search, comments, profiles, sports, GraphQL | None |
| CLOB | clob.polymarket.com | Trading, order books, price history, heartbeat, batch orders | API key |
| Data | data-api.polymarket.com | Positions, P&L, activity, trades, leaderboard, open interest | None (public) |
| RTDS | wss://ws-live-data.polymarket.com | Live comments, crypto prices (BTC/ETH/SOL/XRP) | None |
| Bridge | bridge.polymarket.com | Cross-chain deposits/withdrawals (EVM, Solana, Bitcoin) | Wallet |

## Safety

- Trades preview by default. Nothing executes without `--confirm`.
- This is real money (USDC on Polygon). The Polymarket CLI is experimental software.
- Your private key lives in `~/.config/polymarket/config.json`. Keep it safe.
- Check the order book before placing large orders in low-volume markets.
- Heartbeat API: missed heartbeats (>10s) auto-cancel all resting orders.

## Version

v3.0.0 - Data API (positions, P&L, leaderboard, open interest), RTDS WebSocket (live comments, crypto prices), Bridge API (cross-chain deposits/withdrawals), CLOB additions (heartbeat, post-only, batch orders, spread, fee-rate), Gamma additions (comments, profiles, series, sports, GraphQL), CLI corrected to Rust binary via Homebrew, new market types (5-minute crypto, sports).

## License

MIT
