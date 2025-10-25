try:
    from patterns.strategy import Strategy
    from patterns.observer import SignalPublisher
    from patterns.command import Command, ExecuteOrderCommand, CommandInvoker
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file ./patterns. Error:{e}')

try:
    from data_loader import MarketDataPoint
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file data_loader.py. Error:{e}')
try:
    from models import PortfolioGroup
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file models.py. Error:{e}')

class TradingEngine(SignalPublisher):# [observers]

    def __init__(self, strategy: Strategy, portfolio: PortfolioGroup):
        super().__init__()
        self._strategy = strategy
        self._portfolio = portfolio
        self._command_invoker = CommandInvoker()
        self._pending_signals = []

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def process_tick(self, tick: MarketDataPoint):
        print(f"\nEngine processing tick: {tick}")

        if self._pending_signals:
            for signal in self._pending_signals:
                print(f"  -> Executing pending signal from previous tick: {signal}")
                signal['price'] = tick.price
                command = ExecuteOrderCommand(self._portfolio, signal)
                self._command_invoker.execute_command(command)

            self._pending_signals.clear()

        new_signals = self._strategy.generate_signals(tick)
        if new_signals:
            print(f"  -> Strategy generated new signals: {new_signals}")
            for signal in new_signals:
                self.notify(signal)
            self._pending_signals.extend(new_signals)

    def undo_last_trade(self):
        self._command_invoker.undo_last_command()