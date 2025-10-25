try:
    from patterns.observer import Observer
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please implement source observer.py. Error: {e}')
from typing import Dict

class LoggerObserver(Observer):
    def update(self,signal:Dict):
        print(f"[LOG] Signal Received: {signal}")

class AlertObserver(Observer):
    def __init__(self,large_trade_threshold:int = 10000):
        self.threshold = large_trade_threshold

    def update(self, signal: Dict):
        trade_value = signal.get('quantity', 1) * signal.get('price', 0)
        if trade_value > self.threshold:
            print(f"[ALERT] Large trade detected! Value: ${trade_value:.2f}, Signal: {signal}")