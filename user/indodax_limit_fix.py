"""
Indodax hot-fixes for OctoBot
1.  remove bogus 10 000-IDR price.min
2.  rebuild quoteVolume when Indodax omits it
"""
import ccxt, functools

# ---- 1) patch fetch_markets --------------------------------------
def _patch_limits(cls):
    orig = cls.fetch_markets
    @functools.wraps(orig)
    def fixed(self, params={}):
        mkts = orig(self, params)
        for m in mkts:
            if m["quote"] == "IDR":
                m["limits"]["price"]["min"] = None
                m["limits"]["cost"]["min"]  = 10_000      # real rule
        return mkts
    cls.fetch_markets = fixed

# ---- 2) patch parse_ticker ---------------------------------------
def _patch_ticker(cls):
    orig = cls.parse_ticker
    def fixed(self, t, market=None):
        r = orig(self, t, market)
        if (r.get("baseVolume") not in (None, self.nan)
                and r.get("quoteVolume") in (None, self.nan)
                and r.get("last") not in (None, self.nan)):
            r["quoteVolume"] = r["baseVolume"] * r["last"]
        return r
    cls.parse_ticker = fixed

for C in (ccxt.indodax.indodax,):
    _patch_limits(C); _patch_ticker(C)

# async version (OctoBot sometimes uses it)
try:
    import ccxt.async_support as ax
    for C in (ax.indodax.indodax,):
        _patch_limits(C); _patch_ticker(C)
except ImportError:
    pass
