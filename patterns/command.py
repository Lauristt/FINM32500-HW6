from typing import List, Dict
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

class ExecuteOrderCommand(Command):
    """Execute Trade"""
    def __init__(self, portfolio, signal: Dict):
        self.portfolio = portfolio
        self.signal = signal
        self.trade_quantity = 10
        self.quantity_change = 0# used to revert trade

    def execute(self):
        action = self.signal['action']
        symbol = self.signal['symbol']
        price = self.signal['price']
        print(f"[COMMAND] Executing {action} for {self.trade_quantity} shares of {symbol}...")

        if action == 'BUY':
            self.quantity_change = self.trade_quantity
        elif action == 'SELL':
            self.quantity_change = -self.trade_quantity

        if self.quantity_change != 0:
            self.portfolio.transact(symbol, self.quantity_change, price)

        print(f"  -> Trade Executed.")

    def undo(self):
        symbol = self.signal['symbol']
        price = self.signal['price']
        undo_quantity_change = -self.quantity_change  # this assumes we have already executed transaction
        action = self.signal['action']
        print(f"[COMMAND] Undoing {action} for {symbol}...")
        if undo_quantity_change != 0:
            self.portfolio.transact(symbol, undo_quantity_change, price)
        print(f"  -> Undo Executed.")

class CommandInvoker():
    def __init__(self):
        self._history: List[Command] = []
    def execute_command(self, command: Command):
        self._history.append(command)
        command.execute()

    def undo_last_command(self):
        if self._history:
            last_command = self._history.pop()
            last_command.undo()
        else:
            print("[COMMAND] No commands to undo.")