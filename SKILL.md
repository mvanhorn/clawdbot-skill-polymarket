---
name: polymarket
version: "3.0.0"
description: "Polymarket prediction markets at your fingertips - check odds, track portfolios, research markets with AI-powered analysis, compare markets, and trade. Covers all 4 Polymarket APIs: Gamma, CLOB, Data API, RTDS WebSocket, and Bridge. Read-only works instantly (no setup). The most comprehensive prediction markets skill on ClawHub."
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-polymarket
homepage: https://polymarket.com
metadata:
  openclaw:
    emoji: "📊"
    tags:
      - prediction-markets
      - polymarket
      - trading
      - odds
      - betting
      - forecasting
      - probabilities
      - portfolio
      - research
      - crypto
      - politics
      - sports
      - finance
      - websocket
      - bridge
      - data-api
    triggers:
      - polymarket
      - prediction market
      - prediction markets
      - what are the odds
      - market odds
      - betting odds
      - check odds
      - trending markets
      - market research
      - compare markets
      - portfolio positions
      - open positions
      - trade on polymarket
      - buy shares
      - sell shares
      - polymarket leaderboard
      - polymarket deposit
      - polymarket withdraw
      - crypto prices live
---

# Polymarket

Query [Polymarket](https://polymarket.com) prediction markets and trade from the terminal. Browse odds, research events, compare markets, track your portfolio, stream live data, bridge funds, and execute trades - all through natural language.

Polymarket exposes 4 separate APIs plus the Gamma convenience layer. This skill covers all of them.

## Setup

**Read-only commands work immediately** (no install needed). Browsing, searching, trending, categories, market research, and comparison mode all use the public Gamma API.

For trading, order books, price history, and advanced features, install the [Polymarket CLI](https://github.com/Polymarket/polymarket-cli) (Rust binary, v0.1.5+):

```bash
brew install polymarket/tap/polymarket-cli
```

For trading, set up a wallet:

```bash
polymarket wallet create
polymarket approve set
```

Or manually configure `~/.config/polymarket/config.json` with your private key. See the [CLI docs](https://github.com/Polymarket/polymarket-cli) for details.

The CLI also provides an interactive REPL:

```bash
polymarket shell
```

Use `--output json` on any CLI command for machine-readable output suitable for scripting and piping.

## Commands

### Browse Markets (no CLI needed)

```bash
# Trending/active markets (sorted by 24h volume)
python3 {baseDir}/scripts/polymarket.py trending

# Trending with more results
python3 {baseDir}/scripts/polymarket.py trending --limit 20

# Search markets by keyword
python3 {baseDir}/scripts/polymarket.py search "trump"

# Get specific event by slug
python3 {baseDir}/scripts/polymarket.py event "fed-decision-in-october"

# Get markets by category
python3 {baseDir}/scripts/polymarket.py category politics
python3 {baseDir}/scripts/polymarket.py category crypto
python3 {baseDir}/scripts/polymarket.py category sports
python3 {baseDir}/scripts/polymarket.py category tech
python3 {baseDir}/scripts/polymarket.py category entertainment
python3 {baseDir}/scripts/polymarket.py category science
python3 {baseDir}/scripts/polymarket.py category business
```

### Trending Markets Dashboard (no CLI needed)

Show a categorized dashboard of the hottest markets across Polymarket. Combine trending with category filters to build a full overview.

```bash
# Full trending dashboard - run these in sequence to build a picture:
python3 {baseDir}/scripts/polymarket.py trending --limit 10
python3 {baseDir}/scripts/polymarket.py category politics --limit 5
python3 {baseDir}/scripts/polymarket.py category crypto --limit 5
python3 {baseDir}/scripts/polymarket.py category sports --limit 5
python3 {baseDir}/scripts/polymarket.py category tech --limit 5
```

When the user asks for a "dashboard" or "overview," run all category queries and present the results grouped by section with clear headings. Include volume and current odds for each market.

### Market Research Mode (no CLI needed)

Market research combines Polymarket odds with contextual analysis. When the user asks to "research" a market or wants deeper analysis beyond just odds:

1. **Fetch the market data** using search or event commands
2. **Analyze the odds** - what does the market imply? Is there an edge?
3. **Provide context** - use your knowledge to explain what drives the odds
4. **Show historical movement** - if CLI is available, pull price history
5. **Compare to consensus** - how do Polymarket odds compare to polls, expert opinion, or other prediction markets?

```bash
# Step 1: Find the market
python3 {baseDir}/scripts/polymarket.py search "fed rate cut"

# Step 2: Get detailed event data
python3 {baseDir}/scripts/polymarket.py event "fed-rate-decision-march-2026"

# Step 3: If CLI available, get price history to show trend
python3 {baseDir}/scripts/polymarket.py price-history TOKEN_ID --interval 1d

# Step 4: Check order book depth for liquidity assessment
python3 {baseDir}/scripts/polymarket.py book TOKEN_ID
```

After gathering data, synthesize the research into a structured report:

- **Current Odds**: Yes/No percentages and what they imply
- **Volume & Liquidity**: How much money is in this market, is it liquid enough to trade?
- **Trend**: Are odds moving up or down? Any recent spikes?
- **Context**: What real-world events or data points are driving the odds?
- **Key Dates**: When does the market resolve? Any upcoming catalysts?
- **Risk Factors**: What could cause a sudden move?

### Market Comparison Mode (no CLI needed)

Compare related markets side-by-side. Useful for finding arbitrage, understanding conditional probabilities, or just seeing how different outcomes relate.

```bash
# Compare two or more related markets by searching for each
python3 {baseDir}/scripts/polymarket.py search "trump 2028"
python3 {baseDir}/scripts/polymarket.py search "desantis 2028"
python3 {baseDir}/scripts/polymarket.py search "newsom 2028"
```

When the user asks to "compare markets" or "side-by-side odds":

1. Search for each market the user mentions
2. Present odds in a comparison table format
3. Note volume differences (higher volume = more reliable odds)
4. Flag any apparent inconsistencies (e.g., probabilities that should sum to ~100% but don't)
5. Highlight the spread between related outcomes

Format the comparison as a table:

```
Market Comparison: 2028 Presidential Election

| Candidate     | Yes     | Volume  | Liquidity |
|---------------|---------|---------|-----------|
| Trump         | 32.5%   | $4.2M   | High      |
| DeSantis      | 18.1%   | $1.8M   | Medium    |
| Newsom        | 12.4%   | $890K   | Medium    |
| Harris        | 8.7%    | $2.1M   | Medium    |
```

### Portfolio Dashboard (CLI + wallet required)

View your complete portfolio with positions, P&L, and open orders in one view.

```bash
# View all open positions
python3 {baseDir}/scripts/polymarket.py positions

# View positions for a specific wallet
python3 {baseDir}/scripts/polymarket.py positions --address 0xYOUR_WALLET

# Check USDC balance
python3 {baseDir}/scripts/polymarket.py wallet-balance

# Check balance for a specific token
python3 {baseDir}/scripts/polymarket.py wallet-balance --token TOKEN_ID

# List all open orders
python3 {baseDir}/scripts/polymarket.py orders
```

When the user asks for a "portfolio dashboard" or "how am I doing," run all three commands (positions, wallet-balance, orders) and present a unified view:

- **Positions**: Each position with current market price, your entry price (if available), and unrealized P&L
- **USDC Balance**: Available cash for new trades
- **Open Orders**: Pending limit orders with price and size
- **Total Portfolio Value**: Sum of positions + USDC balance

### Order Book & Prices (CLI required, no wallet)

```bash
# Order book for a token
python3 {baseDir}/scripts/polymarket.py book TOKEN_ID

# Price history (intervals: 1m, 1h, 6h, 1d, 1w, max)
python3 {baseDir}/scripts/polymarket.py price-history TOKEN_ID --interval 1d

# Price history with specific number of data points
python3 {baseDir}/scripts/polymarket.py price-history TOKEN_ID --interval 1h --fidelity 48
```

### Wallet (CLI required)

```bash
polymarket wallet create
polymarket wallet show
polymarket wallet balance
polymarket wallet balance --token TOKEN_ID
```

### Trading (CLI + wallet required)

All trades require `--confirm` to execute. Without it, the order is previewed only. This is a safety feature - you always see what will happen before it happens.

#### Cost & Fee Transparency

Before executing any trade, the skill displays:

- **Order type**: Limit or Market
- **Side**: Buy or Sell
- **Price**: Your limit price (or "market" for market orders)
- **Size**: Number of shares
- **Estimated cost**: Price x Size for limit orders, or dollar amount for market orders
- **Polymarket fee**: Polymarket charges no trading fees on the CLOB (Central Limit Order Book)
- **Gas fees**: On-chain operations (approvals, splits, redeems) require MATIC for gas on Polygon. Typical gas: $0.01-0.05

```bash
# Preview a limit order (no --confirm = preview only)
python3 {baseDir}/scripts/polymarket.py trade buy --token TOKEN_ID --price 0.50 --size 10

# Execute a limit order
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --price 0.50 --size 10

# Sell limit order
python3 {baseDir}/scripts/polymarket.py --confirm trade sell --token TOKEN_ID --price 0.70 --size 10

# Market order: buy $5 worth at current price
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --market-order --amount 5

# Post-only limit order (rests on book only, never takes liquidity - Jan 2026+)
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --price 0.45 --size 20 --post-only
```

### Orders & Positions (CLI + wallet required)

```bash
# List open orders
python3 {baseDir}/scripts/polymarket.py orders

# Cancel a specific order
python3 {baseDir}/scripts/polymarket.py --confirm orders --cancel ORDER_ID

# Cancel all orders
python3 {baseDir}/scripts/polymarket.py --confirm orders --cancel all

# View positions
python3 {baseDir}/scripts/polymarket.py positions
python3 {baseDir}/scripts/polymarket.py positions --address 0xYOUR_WALLET
```

---

## API Reference

Polymarket exposes 4 distinct APIs plus the Gamma convenience layer. Each serves a different purpose.

### 1. Gamma API (gamma-api.polymarket.com) - Public, no auth

The high-level convenience API for browsing and searching markets. Used by all read-only commands.

- **Base URL**: `https://gamma-api.polymarket.com`
- `GET /events` - List events (params: `order`, `ascending`, `closed`, `limit`, `tag_slug`)
- `GET /search` - Search markets (params: `query`, `limit`)
- `GET /events/slug/{slug}` - Event by slug
- `GET /comments` - List and filter comments on markets
- `GET /profiles/{address}` - Public user profiles
- `GET /series` - Grouped event collections (e.g., "2028 Election" series)
- `GET /sports` - Sports metadata including teams, matches, and resolution criteria
- **GraphQL**: `POST /query` - Full GraphQL endpoint with subscription support

### 2. CLOB API (clob.polymarket.com) - Trading

The Central Limit Order Book API for all trading operations. Wrapped by the Polymarket CLI.

- **Base URL**: `https://clob.polymarket.com`
- `GET /prices-history` - Historical prices (intervals: `1m`, `1h`, `6h`, `1d`, `1w`, `max`)
- `GET /spread` - Bid-ask spread for a token
- `GET /fee-rate` - Fee structure details
- `GET /rewards` - Daily maker/taker earnings
- `POST /order` - Place an order
- `POST /orders` - Batch orders (up to 15 per request)
- `DELETE /order/{id}` - Cancel an order
- **Order scoring** - Check maker rebate eligibility before placing orders
- **Post-Only orders** (Jan 2026) - Orders that rest on the book only, never cross the spread
- **Heartbeat API** (Jan 2026):
  - `POST /heartbeat` - Must send within 10 seconds or all open orders auto-cancel
  - Used by market makers to maintain order presence
  - If heartbeat lapses, all resting orders for that API key are cancelled

### 3. Data API (data-api.polymarket.com) - Portfolio & Analytics

The dedicated API for portfolio tracking, trade history, and market analytics. No auth needed for public endpoints.

- **Base URL**: `https://data-api.polymarket.com`
- `GET /positions?user={address}` - Current open positions
  - Sort by: `TOKENS`, `CURRENT`, `INITIAL`, `CASHPNL`, `PERCENTPNL`
- `GET /closed-positions?user={address}` - Historical closed positions
- `GET /activity?user={address}` - Activity feed
  - Types: `TRADE`, `SPLIT`, `MERGE`, `REDEEM`, `REWARD`
- `GET /value?user={address}` - Portfolio valuation in USD
- `GET /trades` - Trade history
  - Filter by: `user`, `market`, `side`
  - Max 500 results per page
- `GET /holders?market={conditionId}` - Top token holders for a market
- `GET /oi` - Open interest across markets
- `GET /volume` - Trading volume across markets
- `GET /leaderboard` - Trader rankings (configurable time period)

Use the Data API for portfolio dashboards and analytics. It provides richer position data than the CLOB API, including P&L calculations and activity history.

### 4. RTDS WebSocket (wss://ws-live-data.polymarket.com) - Real-time Streaming

Real-time data streaming via WebSocket. Subscribe to topics for live updates without polling.

- **URL**: `wss://ws-live-data.polymarket.com`
- **Protocol**: JSON messages over WebSocket
- **Topics**:
  - `comments` - Real-time comment activity
    - Events: `comment_created`, `comment_removed`, `reaction_created`, `reaction_removed`
  - `crypto_prices` - Real-time cryptocurrency prices
    - Assets: BTC, ETH, SOL, XRP
    - Sources: Binance + Chainlink oracles
- **Dynamic subscription management** - Subscribe and unsubscribe to topics on the fly within a single connection
- Useful for building live dashboards, monitoring comment sentiment, or tracking crypto prices that feed into 5-minute crypto markets

### 5. Bridge API (bridge.polymarket.com) - Cross-chain Deposits & Withdrawals

Bridge funds into and out of Polymarket across multiple chains.

- **Base URL**: `https://bridge.polymarket.com`
- `POST /deposit` - Generate deposit addresses
  - Supported chains: EVM (Ethereum, Polygon, Arbitrum, etc.), Solana, Bitcoin
  - Returns a unique deposit address for the selected chain
- `POST /withdraw` (Jan 2026) - Bridge USDC.e to any supported chain
- `GET /supported-assets` - List all supported assets and chains
- `GET /quote` - Get cross-chain bridging quotes (fees, estimated time)

Use the Bridge API when a user needs to move funds in or out of Polymarket without leaving the terminal.

---

## New Market Types

- **5-minute crypto markets** (Feb 2026) - Ultra-short-duration markets on BTC/ETH/SOL price movements. Fed by RTDS crypto_prices data.
- **Sports markets** - Dedicated sports metadata via Gamma `/sports` endpoint with team info, match schedules, and resolution criteria.

## Error Recovery

### API Errors (Gamma API)

If the Gamma API returns an error or is unreachable:

- **HTTP 429 (Rate Limited)**: Wait 5-10 seconds and retry. The Gamma API has generous rate limits but can throttle during high-traffic events.
- **HTTP 500/502/503**: The API is temporarily down. Inform the user and suggest trying again in a minute.
- **Connection Error**: Check internet connectivity. The API endpoint is `https://gamma-api.polymarket.com`.
- **Empty Results**: The search might be too specific. Suggest broader search terms or browse by category instead.

### Data API Errors

- **HTTP 400 (Bad Request)**: Check the `user` address format (must be a valid Ethereum address) or sort parameter spelling.
- **Empty positions**: The address may have no open positions, or the address format may be wrong. Try with and without checksum casing.
- **Pagination**: Trades endpoint maxes at 500 per page. Use cursor-based pagination for full history.

### CLOB API Errors

- **Heartbeat timeout**: If using the Heartbeat API and the connection lapses for >10 seconds, all orders auto-cancel. Reconnect and re-place orders.
- **Post-Only rejection**: A post-only order that would cross the spread is rejected instead of filling. Adjust price to rest on the book.
- **Batch limit**: Maximum 15 orders per batch request. Split larger batches.

### Bridge API Errors

- **Unsupported chain**: Check `/supported-assets` for current chain support.
- **Quote expired**: Bridge quotes have a TTL. Fetch a fresh quote before executing.
- **Minimum amount**: Some chains have minimum deposit/withdrawal amounts.

### CLI Errors

If the Polymarket CLI returns an error:

- **"CLI not installed"**: Install with `brew install polymarket/tap/polymarket-cli`.
- **"Config not found"**: The user needs to run `polymarket wallet create` first.
- **"Insufficient balance"**: Show current balance and the required amount.
- **"Order rejected"**: The price may be outside valid range (0-1) or the market may be closed/resolved.
- **"Approval needed"**: Some operations require a one-time on-chain approval. Run: `polymarket approve set`
- **Timeout**: CLI commands have a 30-second timeout. If a command times out, it may be a network issue or the Polygon RPC may be slow.

### WebSocket Errors

- **Connection dropped**: RTDS WebSocket may drop on network changes. Reconnect and re-subscribe to topics.
- **Invalid topic**: Check available topics. Only `comments` and `crypto_prices` are currently supported.

### Market Not Found

If a market slug or event is not found:

1. Search for the market by keyword instead of slug
2. Check if the market has resolved (use `closed: true` parameter)
3. Suggest similar markets based on the search terms
4. Link to polymarket.com for manual browsing

### Authentication Issues

- **No wallet configured**: Guide the user through `polymarket wallet create`
- **Wrong network**: Polymarket uses Polygon. Ensure the wallet is on the correct network.
- **Insufficient MATIC**: On-chain operations need MATIC for gas. Direct user to bridge or purchase MATIC.

## Usage Examples

### Example 1: Quick odds check

**User**: "What are the odds Trump wins 2028?"

```bash
python3 {baseDir}/scripts/polymarket.py search "trump 2028 president"
```

**Output**:
```
Search: 'trump 2028 president'

  Trump wins 2028 Presidential Election
   Yes: 31.2% | No: 68.8%
   Volume: $4.2M
   Ends: Nov 05, 2028
   polymarket.com/event/trump-wins-2028-presidential-election
```

### Example 2: Trending dashboard

**User**: "What's hot on Polymarket right now?"

Run trending and present top markets grouped by volume:

```
Trending on Polymarket

  Fed Rate Decision - March 2026
   Markets: 3
   - Rate cut: 72.3%
   - No change: 25.1%
   - Rate hike: 2.6%
   Total Volume: $8.1M

  Bitcoin above $150K by July 2026
   Yes: 28.4% | No: 71.6%
   Volume: $3.9M

  UFC 310 Main Event Winner
   Fighter A: 62.1% | Fighter B: 37.9%
   Volume: $1.2M
```

### Example 3: Market research

**User**: "Research the Fed rate decision market for me"

The skill fetches market data, then provides analysis:

```
Market Research: Fed Rate Decision - March 2026

Current Odds:
  Rate cut:    72.3% (down from 81% last week)
  No change:   25.1% (up from 17% last week)
  Rate hike:    2.6% (stable)

Volume & Liquidity:
  Total Volume: $8.1M
  24h Volume:   $420K
  Order book depth: Deep (>$50K on both sides)

Trend: Odds of a cut have fallen ~9 points in the past week,
likely driven by stronger-than-expected jobs report on Friday.

Key Dates:
  - FOMC Meeting: March 18-19, 2026
  - Market resolves: March 19, 2026

Context: The market is pricing in a ~72% chance of a 25bp cut.
This aligns roughly with CME FedWatch tool (68%) and economist
consensus (65-75% for a cut). The slight premium on Polymarket
may reflect retail sentiment skewing more dovish.
```

### Example 4: Portfolio via Data API

**User**: "How's my Polymarket portfolio doing?"

Use the Data API for rich portfolio data:

```bash
# Portfolio value
curl -s "https://data-api.polymarket.com/value?user=0xYOUR_WALLET"

# Open positions sorted by P&L
curl -s "https://data-api.polymarket.com/positions?user=0xYOUR_WALLET&sortBy=CASHPNL"

# Recent activity
curl -s "https://data-api.polymarket.com/activity?user=0xYOUR_WALLET"
```

**Output**:
```
Portfolio Dashboard

Portfolio Value: $289.80

Positions (sorted by P&L):
  Fed Rate Cut (Yes)     100 shares @ $0.65    Current: $0.72    P&L: +$7.00
  BTC > $150K July (No)   50 shares @ $0.60    Current: $0.71    P&L: +$5.50

Recent Activity:
  TRADE  Bought 25 Fed Rate Cut (Yes) @ $0.68    2 hours ago
  REDEEM Claimed $12.40 from resolved market     1 day ago

USDC Balance: $142.30
Open Orders: 1 pending
```

### Example 5: Side-by-side comparison

**User**: "Compare the Republican primary candidates"

```
Market Comparison: 2028 Republican Primary

| Candidate     | Win Primary | Win General | Volume (Primary) |
|---------------|-------------|-------------|------------------|
| Trump         | 42.1%       | 31.2%       | $2.8M            |
| DeSantis      | 22.5%       | 18.1%       | $1.4M            |
| Haley         | 11.3%       |  8.9%       | $680K            |
| Ramaswamy     |  6.8%       |  4.2%       | $320K            |

Note: Primary odds sum to ~95% (gap = long-tail candidates).
Win-general odds are conditional on winning the primary.
```

### Example 6: Trade with cost preview

**User**: "Buy 50 shares of Yes on the Fed rate cut at 68 cents"

```bash
python3 {baseDir}/scripts/polymarket.py trade buy --token TOKEN_ID --price 0.68 --size 50
```

**Output**:
```
Buy Limit Order (PREVIEW)
   Token: Fed Rate Decision - Rate Cut (Yes)
   Side:  BUY
   Price: $0.68
   Size:  50 shares
   Estimated Cost: $34.00
   Trading Fee: $0.00 (Polymarket CLOB has no trading fees)
   Gas Fee: ~$0.01-0.05 MATIC (only on first approval)

   Add --confirm to execute this trade.
   This involves REAL MONEY on Polygon.
```

### Example 7: Leaderboard and top holders

**User**: "Who are the top Polymarket traders?"

```bash
# Trader leaderboard
curl -s "https://data-api.polymarket.com/leaderboard"

# Top holders for a specific market
curl -s "https://data-api.polymarket.com/holders?market=CONDITION_ID"
```

### Example 8: Bridge funds in

**User**: "I want to deposit funds to Polymarket from Ethereum"

```bash
# Check supported assets
curl -s "https://bridge.polymarket.com/supported-assets"

# Get a quote
curl -s -X POST "https://bridge.polymarket.com/deposit" \
  -H "Content-Type: application/json" \
  -d '{"chain": "ethereum", "asset": "USDC"}'
```

### Example 9: Historical price analysis

**User**: "Show me the price history for this market over the past week"

```bash
# Via CLOB API
curl -s "https://clob.polymarket.com/prices-history?tokenID=TOKEN_ID&interval=1d&fidelity=7"

# Or via CLI
polymarket price-history TOKEN_ID --interval 1d --output json
```

### Example 10: Spread and fee check

**User**: "What's the spread on this market?"

```bash
# Bid-ask spread
curl -s "https://clob.polymarket.com/spread?tokenID=TOKEN_ID"

# Fee rate
curl -s "https://clob.polymarket.com/fee-rate"
```

## Safety Notes

- **Real money.** Trades execute on Polygon with real USDC. Double-check everything.
- **All trades require `--confirm`.** Without it, you get a preview only. This is non-negotiable.
- **The CLI is experimental.** The Polymarket team warns: "Use at your own risk and do not use with large amounts of funds."
- **Private key security.** Your key is stored in `~/.config/polymarket/config.json`. Never share it, never commit it.
- **Gas fees.** On-chain operations (approvals, splits, redeems) require MATIC for gas on Polygon.
- **Heartbeat API.** If you use the heartbeat system for market making, a missed heartbeat (>10s) cancels all your resting orders.
- **Market resolution.** Markets resolve based on the resolution source specified in each market. Check the resolution criteria before trading.
- **Slippage.** Market orders execute at the best available price, which may differ from the displayed price in fast-moving markets.
- **Liquidity.** Low-volume markets may have wide bid-ask spreads. Check the order book before placing large orders.
- **Bridge funds.** Cross-chain bridging involves smart contract risk. Verify addresses and amounts before confirming.

## Related Skills

Looking for more market intelligence? Try these OpenClaw skills:

- **/search-x** - Search X/Twitter for real-time sentiment on any topic. Pair with Polymarket odds to gauge whether the market is ahead of or behind public opinion.
- **/last30days** - Deep research on any topic using web + social sources. Use it to build context before placing a trade.
- **/parallel** - Run multiple research tasks simultaneously. Combine Polymarket odds with news, social sentiment, and expert analysis in one shot.
