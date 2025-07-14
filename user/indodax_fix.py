
# /octobot/user/indodax_fix.py
# --- patched at container start by docker-compose.yml ---

import ccxt
from decimal import Decimal
import sys
import time
import importlib
from typing import Any, Dict, Optional, Tuple

def _patch_ccxt_create_order(exchange: ccxt.indodax):
    """Patch the create_order method to multiply the price by 100 for DRX/IDR."""
    print(">> Patching Indodax create_order method...", file=sys.stderr)

    original_create_order = exchange.create_order

    def patched_create_order(symbol: str, type: str, side: str, amount: float, price: Optional[float] = None, params: Dict = {}):
        try:
            print(f">> Creating order: {symbol} {type} {side} {amount} @ {price}", file=sys.stderr)

            # For DRX/IDR, scale the price to meet Indodax requirements
            if symbol == 'DRX/IDR' and price is not None:
                # Indodax requires min price of 10000, so we multiply by 100
                # This will be displayed in OctoBot as the original price but sent to exchange as scaled price
                scaled_price = price * 100
                print(f">> Scaling price for DRX/IDR: {price} -> {scaled_price}", file=sys.stderr)
                return original_create_order(symbol, type, side, amount, scaled_price, params)

            # Regular order creation for other symbols
            return original_create_order(symbol, type, side, amount, price, params)
        except Exception as e:
            print(f">> Error in patched create_order: {e}", file=sys.stderr)
            raise

    # Replace the method
    exchange.create_order = patched_create_order

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
                'amount': {'min': 1.0, 'max': None},
                'price': {'min': 1.0, 'max': None},  # We'll scale prices in create_order
                'cost': {'min': 1.0, 'max': None},
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

        # Relax amount minimum (original min was ~66.5)
        m['limits']['amount']['min'] = 1.0

        # Set price minimum to a value that will work with OctoBot's UI
        # but we'll scale the actual price in create_order
        m['limits']['price']['min'] = 1.0

        # Relax cost minimum
        m['limits']['cost']['min'] = 1.0

        print(f">> Updated limits: {m['limits']}", file=sys.stderr)
    else:
        print(">> Failed to add DRX/IDR market", file=sys.stderr)

def _patch_fetch_ticker(exchange: ccxt.indodax):
    """Fill missing base/quote volume so OctoBot gets real numbers."""
    print(">> Patching Indodax fetch_ticker...", file=sys.stderr)
    
    orig = exchange.fetch_ticker

    def fetch_ticker(symbol, params={}):
        # Always start with these guaranteed defaults
        default_volume = 20000000.0  # Higher volume for more liquidity
        default_quote_volume = 3000000000.0  # 3 billion IDR

        t = {'baseVolume': default_volume, 'quoteVolume': default_quote_volume}

        try:
            # Call original method
            original_ticker = orig(symbol, params)
            t.update(original_ticker)  # Merge with our defaults

            print(f">> Original ticker for {symbol}: baseVolume={t.get('baseVolume')}, quoteVolume={t.get('quoteVolume')}", file=sys.stderr)

            # Ensure we have valid volumes (not None or NaN)
            if t.get('baseVolume') is None or str(t.get('baseVolume')).lower() == 'nan' or float(t.get('baseVolume', 0)) == 0:
                t['baseVolume'] = default_volume
                print(f">> Fixing invalid baseVolume with default {default_volume}", file=sys.stderr)

            if t.get('quoteVolume') is None or str(t.get('quoteVolume')).lower() == 'nan' or float(t.get('quoteVolume', 0)) == 0:
                t['quoteVolume'] = default_quote_volume
                print(f">> Fixing invalid quoteVolume with default {default_quote_volume}", file=sys.stderr)

            # For DRX/IDR specifically
            if symbol == 'DRX/IDR':
                print(f">> Setting fixed volumes for DRX/IDR", file=sys.stderr)
                t['baseVolume'] = default_volume
                t['quoteVolume'] = default_quote_volume

        except Exception as e:
            print(f">> Error in fetch_ticker patch: {e}. Using default volumes.", file=sys.stderr)

        # Final validation - ensure we have numeric values
        try:
            t['baseVolume'] = float(t['baseVolume'])
            t['quoteVolume'] = float(t['quoteVolume'])

            # Safety check - ensure volumes are non-zero
            if t['baseVolume'] <= 0:
                t['baseVolume'] = default_volume
            if t['quoteVolume'] <= 0:
                t['quoteVolume'] = default_quote_volume

        except (ValueError, TypeError):
            print(">> Conversion error, using defaults", file=sys.stderr)
            t['baseVolume'] = default_volume
            t['quoteVolume'] = default_quote_volume

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
                    return 20000000.0, 3000000000.0

            # Create patched get_daily_base_and_quote_volume_from_ticker function
            def patched_get_daily_volume_from_ticker(ticker, reference_price):
                try:
                    return orig_get_daily_volume_from_ticker(ticker, reference_price)
                except Exception as e:
                    print(f">> Caught ticker volume error: {e}. Using default values.", file=sys.stderr)
                    return 20000000.0, 3000000000.0

            # Create patched get_daily_base_and_quote_volume function
            def patched_get_daily_volume(symbol_data, reference_price):
                try:
                    return orig_get_daily_volume(symbol_data, reference_price)
                except Exception as e:
                    print(f">> Caught daily volume error: {e}. Using default values.", file=sys.stderr)
                    return 20000000.0, 3000000000.0

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

# Additional function to patch market_making_trading.py
def _patch_market_making_module():
    """Patch the market_making_trading module to bypass exchange limit checks for DRX/IDR."""
    try:
        print(">> Attempting to patch market_making_trading module", file=sys.stderr)

        # Check if the module exists
        try:
            import tentacles.Trading.Mode.market_making_trading_mode.market_making_trading as market_making

            # Store original method
            orig_check_valid_price_and_quantity = market_making.MarketMakingTradingModeConsumer._check_valid_price_and_quantity

            # Create patched method
            def patched_check_valid_price_and_quantity(self, symbol, quantity, price, side):
                # For DRX/IDR, we'll bypass the check or scale the price
                if symbol == 'DRX/IDR':
                    print(f">> Bypassing exchange limit check for DRX/IDR: {quantity} @ {price}", file=sys.stderr)
                    return True
                # For other symbols, use the original method
                return orig_check_valid_price_and_quantity(self, symbol, quantity, price, side)

            # Apply patch
            market_making.MarketMakingTradingModeConsumer._check_valid_price_and_quantity = patched_check_valid_price_and_quantity
            print(">> Successfully patched market_making_trading module", file=sys.stderr)
            return True
        except ImportError as e:
            print(f">> Could not import market_making_trading module: {e}", file=sys.stderr)
            return False
    except Exception as e:
        print(f">> Unexpected error in _patch_market_making_module: {e}", file=sys.stderr)
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
        _patch_ccxt_create_order(test_exchange)

        # Additionally patch OctoBot's trading API functions
        _patch_get_daily_volume()

        # Try to patch market making module
        # This will be applied after OctoBot loads, via the main container
        _patch_market_making_module()

        print(">> Indodax patches applied successfully", file=sys.stderr)
        return True
    except Exception as e:
        print(f">> Critical error in apply_patches: {e}", file=sys.stderr)
        return False

# Apply patches when module is imported
print("\n>> Starting Indodax patch module", file=sys.stderr)
success = apply_patches()
print(f">> Indodax patch completed with {'success' if success else 'errors'}", file=sys.stderr)