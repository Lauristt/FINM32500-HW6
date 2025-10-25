try:
    from data_loader import MarketDataPoint
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broke. Please implement data_loader.py. Error:{e}')
from typing import List, Dict
from abc import ABC, abstractmethod
import collections

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> List[Dict]:
        pass

# Implement Two Strategy
# Problem: Support interchangeable trading strategies.
# Expectations:
# Create abstract Strategy.generate_signals(tick: MarketDataPoint) -> list.
# Implement:
# MeanReversionStrategy
# BreakoutStrategy
# Each maintains internal state and uses parameters from strategy_params.json.
# Demonstrate strategy interchangeability and signal generation.


class MeanReversionStrategy(Strategy):


    def __init__(self, lookback_window: int, threshold: float):
        self.lookback_window = lookback_window
        self.threshold = threshold
        self.prices = {}

        print(f"Initialized MeanReversionStrategy: window={self.lookback_window}, threshold={self.threshold}")

    def generate_signals(self, tick: MarketDataPoint) -> List[Dict]:
        signals = []

        prices_deque = self.prices.setdefault(
            tick.symbol,
            collections.deque(maxlen=self.lookback_window)
        )

        if len(prices_deque) == self.lookback_window:
            moving_average = sum(prices_deque) / self.lookback_window
            current_price = tick.price

            if current_price < moving_average * (1 - self.threshold):
                signals.append({'symbol': tick.symbol, 'action': 'BUY', 'price': current_price})
            elif current_price > moving_average * (1 + self.threshold):
                signals.append({'symbol': tick.symbol, 'action': 'SELL', 'price': current_price})
        prices_deque.append(tick.price)

        return signals


class BreakoutStrategy(Strategy):

    def __init__(self, lookback_window: int, threshold: float):
        self.lookback_window = lookback_window
        self.threshold = threshold
        self.prices = {}

    def generate_signals(self, tick: MarketDataPoint) -> List[Dict]:
        signals = []

        prices_deque = self.prices.setdefault(
            tick.symbol,
            collections.deque(maxlen=self.lookback_window)
        )

        if len(prices_deque) == self.lookback_window:
            highest_high = max(prices_deque)
            current_price = tick.price
            if current_price > highest_high * (1 + self.threshold):
                signals.append({'symbol': tick.symbol, 'action': 'BUY', 'price': current_price})

        prices_deque.append(tick.price)
        return signals