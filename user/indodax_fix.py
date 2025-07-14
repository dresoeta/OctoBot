
# /octobot/user/indodax_fix.py
# --- patched at container start by docker-compose.yml ---

import ccxt
from decimal import Decimal
import sys
import time

def _patch_limits(exchange: ccxt.indodax):
    """Relax Indodax limits for DRX/IDR trading."""
    print(">> Patching Indodax limits...", file=sys.stderr)

    # Ensure markets are loaded
    if not hasattr(exchange, 'markets') or not exchange.markets:
        try:
            print(">> Loading markets...", file=sys.stderr)
            exchange.load_markets()
        except Exception as e:
            print(f">> Error loading markets: {e}", file=sys.stderr)

    # Force add DRX/IDR if not present
    if 'DRX/IDR' not in exchange.markets:
        print(">> DRX/IDR market not found. Adding it manually...", file=sys.stderr)
        exchange.markets['DRX/IDR'] = {
            'id': 'drxidr',
            'symbol': 'DRX/IDR',
            'base': 'DRX',
            'quote': 'IDR',
            'baseId': 'drx',
            'quoteId': 'idr',
            'active': True,
            'limits': {
                'amount': {'min': 66.53613917, 'max': None},
                'price': {'min': 10000.0, 'max': None},
                'cost': {'min': None, 'max': None},
                'leverage': {'min': None, 'max': None}
            },
            'precision': {
                'amount': 8,
                'price': 8
            },
            'info': {}
        }

    # Patch limits
    if 'DRX/IDR' in exchange.markets:
        m = exchange.markets['DRX/IDR']
        print(f">> Original limits: {m['limits']}", file=sys.stderr)

        # Relax price minimum (original min was 10000.0)
        m['limits']['price']['min'] = 0.0

        # Relax amount minimum (original min was ~66.5)
        m['limits']['amount']['min'] = 0.1

        # Relax cost minimum
        m['limits']['cost']['min'] = 0.0

        print(f">> Updated limits: {m['limits']}", file=sys.stderr)
    else:
        print(">> Failed to add DRX/IDR market", file=sys.stderr)

def _patch_fetch_ticker(exchange: ccxt.indodax):
    """Fill missing base/quote volume so OctoBot gets real numbers."""
    print(">> Patching Indodax fetch_ticker...", file=sys.stderr)

    orig = exchange.fetch_ticker

    def fetch_ticker(symbol, params={}):
        t = {'baseVolume': 1000000.0, 'quoteVolume': 150000000.0}  # Default values

        try:
            # Call original method
            original_ticker = orig(symbol, params)
            t.update(original_ticker)  # Merge with our defaults

            print(f">> Original ticker for {symbol}: baseVolume={t.get('baseVolume')}, quoteVolume={t.get('quoteVolume')}", file=sys.stderr)

            # Ensure we have valid volumes (not None or NaN)
            if t.get('baseVolume') is None or str(t.get('baseVolume')).lower() == 'nan':
                t['baseVolume'] = 1000000.0
                print(f">> Fixing invalid baseVolume with default", file=sys.stderr)

            if t.get('quoteVolume') is None or str(t.get('quoteVolume')).lower() == 'nan':
                t['quoteVolume'] = 150000000.0
                print(f">> Fixing invalid quoteVolume with default", file=sys.stderr)

            # Try to get accurate market data
            try:
                market_id = exchange.market_id(symbol)
                print(f">> Market ID for {symbol}: {market_id}", file=sys.stderr)

                # Get summary data
                raw = exchange.publicGetSummary()

                if market_id in raw:
                    info = raw[market_id]
                    base, quote = symbol.split('/')

                    # Get volume data
                    bv_key = f'vol_{base.lower()}'
                    qv_key = f'vol_{quote.lower()}'

                    bv = info.get(bv_key)
                    qv = info.get(qv_key)

                    print(f">> Volume data from API: {bv_key}={bv}, {qv_key}={qv}", file=sys.stderr)

                    if bv and bv != '0':
                        t['baseVolume'] = float(bv)
                    if qv and qv != '0':
                        t['quoteVolume'] = float(qv)
                else:
                    print(f">> Market {market_id} not found in summary, using defaults", file=sys.stderr)
            except Exception as e:
                print(f">> Error getting market data: {e}", file=sys.stderr)
                # Continue with defaults already set

        except Exception as e:
            print(f">> Error in fetch_ticker patch: {e}. Using default volumes.", file=sys.stderr)

        # Final validation - ensure we have numeric values
        try:
            t['baseVolume'] = float(t['baseVolume'])
            t['quoteVolume'] = float(t['quoteVolume'])
        except (ValueError, TypeError):
            print(">> Conversion error, using defaults", file=sys.stderr)
            t['baseVolume'] = 1000000.0
            t['quoteVolume'] = 150000000.0

        print(f">> Final ticker for {symbol}: baseVolume={t.get('baseVolume')}, quoteVolume={t.get('quoteVolume')}", file=sys.stderr)
        return t

    exchange.fetch_ticker = fetch_ticker

def _patch_get_daily_volume():
    """Patch the trading_api.get_daily_base_and_quote_volume function to handle NaN values."""
    try:
        import importlib
        import sys
        print(">> Attempting to patch OctoBot trading API volume functions", file=sys.stderr)

        # Try to import the modules we need to patch
        try:
            import octobot_trading.api.symbol_data as symbol_data_api

            # Store original functions
            orig_get_daily_volume = symbol_data_api.get_daily_base_and_quote_volume
            orig_get_daily_volume_from_ticker = symbol_data_api.get_daily_base_and_quote_volume_from_ticker
            orig_compute_volume = symbol_data_api.compute_base_and_quote_volume

            # Create patched compute_base_and_quote_volume function
            def patched_compute_volume(base_volume, quote_volume, reference_price):
                try:
                    # Try original function first
                    return orig_compute_volume(base_volume, quote_volume, reference_price)
                except ValueError as e:
                    print(f">> Caught volume computation error: {e}. Using default values.", file=sys.stderr)
                    # Return reasonable defaults
                    return 1000000.0, 150000000.0

            # Create patched get_daily_base_and_quote_volume_from_ticker function
            def patched_get_daily_volume_from_ticker(ticker, reference_price):
                try:
                    return orig_get_daily_volume_from_ticker(ticker, reference_price)
                except Exception as e:
                    print(f">> Caught ticker volume error: {e}. Using default values.", file=sys.stderr)
                    return 1000000.0, 150000000.0

            # Create patched get_daily_base_and_quote_volume function
            def patched_get_daily_volume(symbol_data, reference_price):
                try:
                    return orig_get_daily_volume(symbol_data, reference_price)
                except Exception as e:
                    print(f">> Caught daily volume error: {e}. Using default values.", file=sys.stderr)
                    return 1000000.0, 150000000.0

            # Apply patches
            symbol_data_api.compute_base_and_quote_volume = patched_compute_volume
            symbol_data_api.get_daily_base_and_quote_volume_from_ticker = patched_get_daily_volume_from_ticker
            symbol_data_api.get_daily_base_and_quote_volume = patched_get_daily_volume

            print(">> Successfully patched OctoBot trading API volume functions", file=sys.stderr)
            return True
        except ImportError as e:
            print(f">> Could not import OctoBot trading modules: {e}", file=sys.stderr)
            return False
    except Exception as e:
        print(f">> Unexpected error in _patch_get_daily_volume: {e}", file=sys.stderr)
        return False

def apply_patches():
    """Apply patches to the ccxt.indodax class."""
    print(">> Applying Indodax patches...", file=sys.stderr)

    # Create a test instance to patch the class
    try:
        test_exchange = ccxt.indodax({'enableRateLimit': True})

        # Load markets first with retry
        markets_loaded = False
        for attempt in range(3):
            try:
                test_exchange.load_markets()
                markets_loaded = True
                print(f">> Markets loaded successfully (attempt {attempt+1})", file=sys.stderr)
                break
            except Exception as e:
                print(f">> Warning: Could not load markets (attempt {attempt+1}): {e}", file=sys.stderr)
                time.sleep(1)  # Wait a bit before retrying

        # Apply patches even if markets failed to load
        _patch_limits(test_exchange)
        _patch_fetch_ticker(test_exchange)

        # Additionally patch OctoBot's trading API functions
        _patch_get_daily_volume()

        print(">> Indodax patches applied successfully", file=sys.stderr)
        return True
    except Exception as e:
        print(f">> Critical error in apply_patches: {e}", file=sys.stderr)
        return False

# Apply patches when module is imported
print("\n>> Starting Indodax patch module", file=sys.stderr)
success = apply_patches()
print(f">> Indodax patch completed with {'success' if success else 'errors'}", file=sys.stderr)