---
name: polymarket
description: Query Polymarket prediction markets - check odds, trending markets, search events, track prices and momentum.
homepage: https://polymarket.com
metadata: {"clawdbot":{"emoji":"📊"}}
---

# Polymarket

Query [Polymarket](https://polymarket.com) prediction markets. Check odds, find trending markets, search events, track price movements.

## Commands

```bash
# Trending markets (by 24h volume)
python3 {baseDir}/scripts/polymarket.py trending

# Featured/high-profile markets
python3 {baseDir}/scripts/polymarket.py featured

# Search markets (fuzzy matching)
python3 {baseDir}/scripts/polymarket.py search "giannis"
python3 {baseDir}/scripts/polymarket.py search "bitcoin" --all

# Get event by slug or URL
python3 {baseDir}/scripts/polymarket.py event where-will-giannis-be-traded
python3 {baseDir}/scripts/polymarket.py event "https://polymarket.com/event/fed-decision"

# Get specific outcome with details
python3 {baseDir}/scripts/polymarket.py market where-will-giannis-be-traded warriors
python3 {baseDir}/scripts/polymarket.py market 2028-election trump

# Browse by category
python3 {baseDir}/scripts/polymarket.py category politics
python3 {baseDir}/scripts/polymarket.py category crypto
python3 {baseDir}/scripts/polymarket.py category sports
```

## Example Chat Usage

- "What are the odds Giannis gets traded to the Warriors?"
- "Trending on Polymarket?"
- "Search Polymarket for Bitcoin"
- "What's the spread on the Fed rate decision?"
- "Show me the full Giannis trade market"

## Output Features

Markets show:
- **Current odds** (Yes/No prices)
- **Price momentum** (24h/1wk/1mo changes with arrows)
- **Volume** (total + 24h activity)
- **Time remaining** ("Ends in 8d" vs raw date)
- **Bid/ask spread** (liquidity quality indicator)
- **Deep liquidity** (verbose mode)

Multi-outcome events:
- Sorted by odds (highest first)
- Shows top 10 by default, `--all` for complete list
- Volume per outcome

## Options

- `-l, --limit N` - Number of results (default: 5)
- `-a, --all` - Show all outcomes in multi-market events
- `--json` - Raw JSON output

## API

Uses the public Gamma API (no auth required for reading):
- Base URL: `https://gamma-api.polymarket.com`
- Docs: https://docs.polymarket.com

## Tips

- **Slug from URL**: Copy the URL path directly - the script parses it
- **Partial matching**: `event giannis` tries to find matching slugs
- **Specific outcomes**: `market <event> <outcome>` for deep dive on one option
- **Categories**: politics, crypto, sports, tech, entertainment, science, business

## Note

This is read-only. Trading requires wallet authentication (not implemented).
