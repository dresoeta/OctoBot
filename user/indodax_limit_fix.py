# /octobot/user/indodax_fix.py
# --- patched at container start by docker-compose.yml ---

import ccxt
from decimal import Decimal

def _patch_limits(exchange: ccxt.indodax):
    """Relax Indodax limits ⇒ price_min=0 ; keep amount_min (≈65 IDR now)."""
    if 'DRX/IDR' in exchange.markets:
        m = exchange.markets['DRX/IDR']
        m['limits']['price']['min'] = 0
        m['limits']['cost']['min'] = 0

def _patch_fetch_ticker(exchange: ccxt.indodax):
    """Fill missing base/quote volume so OctoBot gets real numbers."""
    orig = exchange.fetch_ticker

    def fetch_ticker(symbol, params={}):
        t = orig(symbol, params)
        market_id = exchange.market_id(symbol)            # e.g. 'drxidr'
        raw = exchange.publicGetSummary()                 # single call, tiny
        if market_id in raw:
            info = raw[market_id]
            # Indodax returns vols in the 24h summary as strings
            base, quote = symbol.split('/')
            bv = info.get(f'vol_{base.lower()}')
            qv = info.get(f'vol_{quote.lower()}')
            if bv:  t['baseVolume']  = float(bv)
            if qv:  t['quoteVolume'] = float(qv)
        return t

    exchange.fetch_ticker = fetch_ticker

# ---- apply both patches on module import ----
ex = ccxt.indodax({'enableRateLimit': True})
_patch_limits(ex)
_patch_fetch_ticker(ex)       # patches the class method, so all instances inherit
print(">> Indodax limits & volume hot-patch loaded")
