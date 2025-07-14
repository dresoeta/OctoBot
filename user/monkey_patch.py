# /octobot/user/monkey_patch.py
# This script patches OctoBot modules at runtime
# It should be imported from docker-compose.yml after OctoBot starts

import sys
import time

print("\n>> Starting OctoBot monkey patching...", file=sys.stderr)

def patch_market_making():
    """Patch the market_making_trading module to bypass exchange limits."""
    try:
        # Wait for tentacles to load
        time.sleep(5)

        # Try to import the module
        try:
            import tentacles.Trading.Mode.market_making_trading_mode.market_making_trading as market_making
            from decimal import Decimal

            # Store original methods
            orig_check_valid = market_making.MarketMakingTradingModeConsumer._check_valid_price_and_quantity
            orig_create_order = market_making.MarketMakingTradingModeConsumer._create_order

            # Create patched methods
            def patched_check_valid(self, symbol, quantity, price, side):
                # Always return True for DRX/IDR
                if symbol == 'DRX/IDR':
                    print(f">> Bypassing exchange limit check for {symbol}: {quantity} @ {price}", file=sys.stderr)
                    return True
                return orig_check_valid(self, symbol, quantity, price, side)

            def patched_create_order(self, order_type, symbol, quantity, price=None):
                # For DRX/IDR, scale the price to meet Indodax requirements
                if symbol == 'DRX/IDR' and price is not None:
                    # Use the original price for display in OctoBot
                    original_price = price
                    # Scale price for the exchange API (will be scaled again in our ccxt patch)
                    scaled_price = Decimal("100.0") * price
                    print(f">> Scaling price for {symbol}: {original_price} -> {scaled_price}", file=sys.stderr)
                    return orig_create_order(self, order_type, symbol, quantity, scaled_price)
                return orig_create_order(self, order_type, symbol, quantity, price)

            # Apply patches
            market_making.MarketMakingTradingModeConsumer._check_valid_price_and_quantity = patched_check_valid
            market_making.MarketMakingTradingModeConsumer._create_order = patched_create_order

            print(">> Successfully patched market_making_trading module", file=sys.stderr)
            return True
        except ImportError as e:
            print(f">> Could not import market_making_trading module: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f">> Error patching market_making_trading: {e}", file=sys.stderr)
            return False
    except Exception as e:
        print(f">> Unexpected error in patch_market_making: {e}", file=sys.stderr)
        return False

def patch_symbol_data():
    """Patch OctoBot's volume calculation to handle NaN values."""
    try:
        # Try to import the modules we need to patch
        try:
            import octobot_trading.api.symbol_data as symbol_data_api
            from decimal import Decimal

            # Create fixed volume calculation
            def fixed_get_volume(symbol_data, reference_price):
                if getattr(symbol_data, "symbol", "") == 'DRX/IDR':
                    print(f">> Using fixed volume for DRX/IDR", file=sys.stderr)
                    return Decimal("20816997"), Decimal("2964099478")
                try:
                    return symbol_data_api.get_daily_base_and_quote_volume(symbol_data, reference_price)
                except Exception as e:
                    print(f">> Error in volume calculation: {e}, using defaults", file=sys.stderr)
                    return Decimal("20816997"), Decimal("2964099478")

            # Replace the function
            import tentacles.Trading.Mode.market_making_trading_mode.market_making_trading as market_making
            original_get_daily_volume = market_making.MarketMakingTradingModeProducer._get_daily_volume

            def patched_get_daily_volume(self, reference_price):
                try:
                    # Try original method
                    return original_get_daily_volume(self, reference_price)
                except ValueError as e:
                    print(f">> Error in _get_daily_volume: {e}, using defaults", file=sys.stderr)
                    # Return fixed values for DRX/IDR
                    return Decimal("20816997"), Decimal("2964099478")

            # Apply patch
            market_making.MarketMakingTradingModeProducer._get_daily_volume = patched_get_daily_volume

            print(">> Successfully patched volume calculation", file=sys.stderr)
            return True
        except ImportError as e:
            print(f">> Could not import required modules: {e}", file=sys.stderr)
            return False
    except Exception as e:
        print(f">> Unexpected error in patch_symbol_data: {e}", file=sys.stderr)
        return False

# Apply patches
success = patch_market_making() and patch_symbol_data()
print(f">> Monkey patching completed with {'success' if success else 'errors'}", file=sys.stderr)
