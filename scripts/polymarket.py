#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
Polymarket prediction market data.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

BASE_URL = "https://gamma-api.polymarket.com"


def fetch(endpoint: str, params: dict = None) -> dict:
    """Fetch from Gamma API."""
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def format_price(price) -> str:
    """Format price as percentage."""
    if price is None:
        return "N/A"
    try:
        pct = float(price) * 100
        return f"{pct:.1f}%"
    except:
        return str(price)


def format_volume(volume) -> str:
    """Format volume in human readable form."""
    if volume is None:
        return "N/A"
    try:
        v = float(volume)
        if v >= 1_000_000:
            return f"${v/1_000_000:.1f}M"
        elif v >= 1_000:
            return f"${v/1_000:.1f}K"
        else:
            return f"${v:.0f}"
    except:
        return str(volume)


def format_change(change) -> str:
    """Format price change with arrow."""
    if change is None:
        return ""
    try:
        c = float(change) * 100
        if c > 0:
            return f"↑{c:.1f}%"
        elif c < 0:
            return f"↓{abs(c):.1f}%"
        else:
            return "→0%"
    except:
        return ""


def format_time_remaining(end_date: str) -> str:
    """Format time remaining until end date."""
    if not end_date:
        return ""
    try:
        dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        delta = dt - now
        
        if delta.days < 0:
            return "Ended"
        elif delta.days == 0:
            hours = delta.seconds // 3600
            if hours == 0:
                mins = delta.seconds // 60
                return f"Ends in {mins}m"
            return f"Ends in {hours}h"
        elif delta.days == 1:
            return "Ends tomorrow"
        elif delta.days < 7:
            return f"Ends in {delta.days}d"
        elif delta.days < 30:
            weeks = delta.days // 7
            return f"Ends in {weeks}w"
        else:
            return dt.strftime('%b %d, %Y')
    except:
        return ""


def extract_slug_from_url(url_or_slug: str) -> str:
    """Extract slug from Polymarket URL or return as-is if already a slug."""
    if 'polymarket.com' in url_or_slug:
        parsed = urlparse(url_or_slug)
        path = parsed.path.strip('/')
        # /event/slug-here -> slug-here
        if path.startswith('event/'):
            return path.replace('event/', '')
        return path
    return url_or_slug


def format_market(market: dict, verbose: bool = False) -> str:
    """Format a single market for display."""
    lines = []
    
    question = market.get('question') or market.get('title', 'Unknown')
    lines.append(f"📊 **{question}**")
    
    # Prices
    prices = market.get('outcomePrices')
    if prices:
        if isinstance(prices, str):
            try:
                prices = json.loads(prices)
            except:
                prices = None
        
        if prices and len(prices) >= 2:
            yes_price = format_price(prices[0])
            no_price = format_price(prices[1])
            
            # Add price changes if available
            day_change = format_change(market.get('oneDayPriceChange'))
            change_str = f" ({day_change})" if day_change else ""
            
            lines.append(f"   Yes: {yes_price}{change_str} | No: {no_price}")
    
    # Bid/ask spread (liquidity indicator)
    bid = market.get('bestBid')
    ask = market.get('bestAsk')
    if bid is not None and ask is not None:
        spread = float(ask) - float(bid)
        if spread > 0:
            lines.append(f"   Spread: {spread*100:.1f}% (Bid: {format_price(bid)} / Ask: {format_price(ask)})")
    
    # Volume
    volume = market.get('volume') or market.get('volumeNum')
    if volume:
        vol_str = f"   Volume: {format_volume(volume)}"
        vol_24h = market.get('volume24hr')
        if vol_24h and float(vol_24h) > 0:
            vol_str += f" (24h: {format_volume(vol_24h)})"
        lines.append(vol_str)
    
    # Time remaining
    end_date = market.get('endDate') or market.get('endDateIso')
    time_left = format_time_remaining(end_date)
    if time_left:
        lines.append(f"   ⏰ {time_left}")
    
    # Verbose mode extras
    if verbose:
        week_change = format_change(market.get('oneWeekPriceChange'))
        month_change = format_change(market.get('oneMonthPriceChange'))
        if week_change or month_change:
            lines.append(f"   📈 1w: {week_change or 'N/A'} | 1m: {month_change or 'N/A'}")
        
        liquidity = market.get('liquidityNum') or market.get('liquidity')
        if liquidity:
            lines.append(f"   💧 Liquidity: {format_volume(liquidity)}")
    
    # Slug for reference
    slug = market.get('slug') or market.get('market_slug')
    if slug:
        lines.append(f"   🔗 polymarket.com/event/{slug}")
    
    return '\n'.join(lines)


def format_event(event: dict, show_all_markets: bool = False) -> str:
    """Format an event with its markets."""
    lines = []
    
    title = event.get('title', 'Unknown Event')
    lines.append(f"🎯 **{title}**")
    
    # Event-level info
    volume = event.get('volume')
    if volume:
        vol_str = f"   Volume: {format_volume(volume)}"
        vol_24h = event.get('volume24hr')
        if vol_24h and float(vol_24h) > 0:
            vol_str += f" (24h: {format_volume(vol_24h)})"
        lines.append(vol_str)
    
    # Time remaining
    end_date = event.get('endDate')
    time_left = format_time_remaining(end_date)
    if time_left:
        lines.append(f"   ⏰ {time_left}")
    
    # Markets in this event - sort by price descending
    markets = event.get('markets', [])
    if markets:
        # Parse and sort markets by Yes price
        market_prices = []
        for m in markets:
            prices = m.get('outcomePrices')
            if prices:
                if isinstance(prices, str):
                    try:
                        prices = json.loads(prices)
                    except:
                        prices = []
                if prices and len(prices) >= 1:
                    try:
                        yes_price = float(prices[0])
                    except:
                        yes_price = 0
                else:
                    yes_price = 0
            else:
                yes_price = 0
            
            # Skip inactive markets with 0 volume
            if not m.get('active', True) and m.get('volumeNum', 0) == 0:
                continue
                
            market_prices.append((m, yes_price))
        
        # Sort by price descending
        market_prices.sort(key=lambda x: x[1], reverse=True)
        
        lines.append(f"   Markets: {len(market_prices)}")
        
        display_count = len(market_prices) if show_all_markets else min(10, len(market_prices))
        for m, price in market_prices[:display_count]:
            name = m.get('groupItemTitle') or m.get('question', '')[:40]
            vol = m.get('volumeNum', 0)
            day_change = format_change(m.get('oneDayPriceChange'))
            change_str = f" {day_change}" if day_change else ""
            
            if price > 0:
                lines.append(f"   • {name}: {format_price(price)}{change_str} ({format_volume(vol)})")
            else:
                lines.append(f"   • {name}")
        
        if len(market_prices) > display_count:
            lines.append(f"   ... and {len(market_prices) - display_count} more")
    
    slug = event.get('slug')
    if slug:
        lines.append(f"   🔗 polymarket.com/event/{slug}")
    
    return '\n'.join(lines)


def cmd_trending(args):
    """Get trending/active markets."""
    params = {
        'order': 'volume24hr',
        'ascending': 'false',
        'closed': 'false',
        'limit': args.limit
    }
    
    data = fetch('/events', params)
    
    print(f"🔥 **Trending on Polymarket**\n")
    
    for event in data:
        print(format_event(event))
        print()


def cmd_featured(args):
    """Get featured markets."""
    params = {
        'closed': 'false',
        'featured': 'true',
        'limit': args.limit
    }
    
    data = fetch('/events', params)
    
    print(f"⭐ **Featured Markets**\n")
    
    if not data:
        # Fallback to high volume
        params = {
            'order': 'volume',
            'ascending': 'false',
            'closed': 'false',
            'limit': args.limit
        }
        data = fetch('/events', params)
        print("(Showing highest volume markets)\n")
    
    for event in data:
        print(format_event(event))
        print()


def cmd_search(args):
    """Search markets with fuzzy matching."""
    query = args.query.lower()
    
    # First try slug-based lookup
    slug_guess = query.replace(' ', '-')
    try:
        data = fetch('/events', {'slug': slug_guess, 'closed': 'false'})
        if data:
            print(f"🔍 **Found: '{args.query}'**\n")
            for event in data[:args.limit]:
                print(format_event(event, show_all_markets=args.all))
                print()
            return
    except:
        pass
    
    # Try partial slug match
    try:
        data = fetch('/events', {'closed': 'false', 'limit': 200})
        matches = []
        
        for event in data:
            slug = event.get('slug', '').lower()
            title = event.get('title', '').lower()
            desc = event.get('description', '').lower()
            
            # Check slug, title, description
            if query in slug or query in title or query in desc:
                matches.append(event)
                continue
            
            # Check individual markets
            for m in event.get('markets', []):
                q = m.get('question', '').lower()
                item = m.get('groupItemTitle', '').lower()
                if query in q or query in item:
                    matches.append(event)
                    break
        
        print(f"🔍 **Search: '{args.query}'**\n")
        
        if not matches:
            print("No markets found.")
            print(f"\nTip: Try the full slug from the URL, e.g.:")
            print(f"  polymarket event where-will-giannis-be-traded")
            return
        
        for event in matches[:args.limit]:
            print(format_event(event, show_all_markets=args.all))
            print()
            
    except Exception as e:
        print(f"Search error: {e}")


def cmd_event(args):
    """Get specific event by slug or URL."""
    slug = extract_slug_from_url(args.slug)
    
    try:
        # Try direct slug lookup
        data = fetch('/events', {'slug': slug})
        
        if not data:
            # Try partial match
            all_events = fetch('/events', {'closed': 'false', 'limit': 200})
            slug_lower = slug.lower()
            matches = [e for e in all_events if slug_lower in e.get('slug', '').lower()]
            
            if matches:
                data = matches
            else:
                print(f"❌ Event not found: {slug}")
                print(f"\nTip: Search for it first:")
                print(f"  polymarket search {slug.split('-')[0]}")
                return
        
        event = data[0] if isinstance(data, list) and data else data
        
        print(format_event(event, show_all_markets=True))
        
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ Event not found: {slug}")
        else:
            raise


def cmd_market(args):
    """Get specific market outcome within an event."""
    slug = extract_slug_from_url(args.slug)
    outcome = args.outcome.lower() if args.outcome else None
    
    try:
        data = fetch('/events', {'slug': slug})
        
        if not data:
            print(f"❌ Event not found: {slug}")
            return
        
        event = data[0] if isinstance(data, list) else data
        markets = event.get('markets', [])
        
        if not outcome:
            # Show all markets
            print(f"🎯 **{event.get('title')}**\n")
            for m in markets:
                print(format_market(m, verbose=True))
                print()
            return
        
        # Find matching market
        for m in markets:
            name = m.get('groupItemTitle', '').lower()
            question = m.get('question', '').lower()
            if outcome in name or outcome in question:
                print(format_market(m, verbose=True))
                return
        
        print(f"❌ Outcome '{args.outcome}' not found")
        print(f"\nAvailable outcomes:")
        for m in markets[:15]:
            name = m.get('groupItemTitle') or m.get('question', '')[:40]
            print(f"  • {name}")
                
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ Event not found: {slug}")
        else:
            raise


def cmd_category(args):
    """Get markets by category."""
    categories = {
        'politics': ['politics', 'election', 'trump', 'biden', 'congress'],
        'crypto': ['crypto', 'bitcoin', 'ethereum', 'btc', 'eth'],
        'sports': ['sports', 'nba', 'nfl', 'mlb', 'soccer'],
        'tech': ['tech', 'ai', 'apple', 'google', 'microsoft'],
        'entertainment': ['entertainment', 'movie', 'oscar', 'grammy'],
        'science': ['science', 'space', 'nasa', 'climate'],
        'business': ['business', 'fed', 'interest', 'stock', 'market']
    }
    
    tags = categories.get(args.category.lower(), [args.category.lower()])
    
    data = fetch('/events', {
        'closed': 'false',
        'limit': 100,
        'order': 'volume24hr',
        'ascending': 'false'
    })
    
    matches = []
    for event in data:
        title = event.get('title', '').lower()
        event_tags = [t.get('label', '').lower() for t in event.get('tags', [])]
        
        for tag in tags:
            if tag in title or tag in ' '.join(event_tags):
                matches.append(event)
                break
    
    print(f"📁 **Category: {args.category.title()}**\n")
    
    if not matches:
        print(f"No markets found for '{args.category}'")
        print(f"\nAvailable categories: politics, crypto, sports, tech, entertainment, science, business")
        return
    
    for event in matches[:args.limit]:
        print(format_event(event))
        print()


def main():
    parser = argparse.ArgumentParser(description="Polymarket prediction markets")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    parser.add_argument("--all", "-a", action="store_true", help="Show all markets in event")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Trending
    subparsers.add_parser("trending", help="Get trending markets")
    
    # Featured
    subparsers.add_parser("featured", help="Get featured markets")
    
    # Search
    search_parser = subparsers.add_parser("search", help="Search markets")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--all", "-a", action="store_true", help="Show all outcomes")
    
    # Event
    event_parser = subparsers.add_parser("event", help="Get event by slug or URL")
    event_parser.add_argument("slug", help="Event slug or polymarket.com URL")
    
    # Market (specific outcome)
    market_parser = subparsers.add_parser("market", help="Get specific market outcome")
    market_parser.add_argument("slug", help="Event slug or URL")
    market_parser.add_argument("outcome", nargs="?", help="Outcome name (e.g. 'warriors')")
    
    # Category
    cat_parser = subparsers.add_parser("category", help="Markets by category")
    cat_parser.add_argument("category", help="Category: politics, crypto, sports, tech, etc.")
    
    args = parser.parse_args()
    
    commands = {
        "trending": cmd_trending,
        "featured": cmd_featured,
        "search": cmd_search,
        "event": cmd_event,
        "market": cmd_market,
        "category": cmd_category,
    }
    
    try:
        commands[args.command](args)
    except requests.RequestException as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
