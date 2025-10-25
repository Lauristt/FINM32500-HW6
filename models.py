from __future__ import annotations
from typing import List, Dict
from abc import abstractmethod

class Instrument():
    def __init__(self,symbol:str,**kwargs):
        self.symbol = symbol
    # use this to print out what type of data this is
    def __repr__(self) -> str:
        return f"Instrument(symbol = '{self.symbol}', name = '{self.name}')"
    def get_metrics(self)->Dict:
        return {'symbol':self.symbol}

class Stock(Instrument):
    def __init__(self,symbol:str,**kwargs):
        super().__init__(symbol=symbol)
        self.type = 'Stock'

class Bond(Instrument):
    def __init__(self,symbol:str,**kwargs):
        super().__init__(symbol=symbol)
        self.type = 'Bond'

class ETF(Instrument):
    def __init__(self,symbol:str,**kwargs):
        super().__init__(symbol=symbol)
        self.type = 'ETF'

@abstractmethod
class PortfolioComponent():
    # basic functions: calculate values and positions
    def get_value(self)->float:
        pass
    def get_positions(self)->List:
        pass

class Position(PortfolioComponent):
    """
    Leaf position component
    """
    # we set the quantity to be int (can it be float for robustness?)
    def __init__(self,symbol:str,quantity:int,price:float):
        self.quantity = quantity
        self.symbol = symbol
        self.price =price
    def get_value(self)->float:
        return self.quantity * self.price
    # positions
    def get_positions(self)->List:
        return [self]
    def __repr__(self) -> str:
        return f"Position(symbol = '{self.symbol}',quantity = '{self.quantity}',value = '{self.get_value():.2f}')"

class PortfolioGroup(PortfolioComponent):
    """
    Combined position component
    """
    def __init__(self,name:str):
        self.name=name
        self.owner = None
        self._children: List[PortfolioComponent] = []
    def add(self,component:PortfolioComponent):
        self._children.append(component)
    def remove(self,component:PortfolioComponent):
        self._children.remove(component)
    def get_value(self)->float:
        return sum(child.get_value() for child in self._children)

    def get_positions(self)->List[Position]:
        positions = []
        for child in self._children:
            #extend a list
            positions.extend(child.get_positions())
        return positions

    def transact(self, symbol: str, quantity_change: int, price: float):
        """Build a simple transact logic"""
        existing_position = None
        for pos in self.get_positions():
            if pos.symbol == symbol:
                existing_position = pos#return a list
                break
        if existing_position:
            print(f"  -> Updating position for {symbol}: quantity change {quantity_change}")
            existing_position.quantity += quantity_change
            if existing_position.quantity <= 0:
                for child in self._children:
                    if isinstance(child, Position) and child.symbol == symbol:
                        self.remove(child)
                        print(f"  -> Position for {symbol} removed from portfolio. Invalid holdings amount. (<0)")
                        break
        elif quantity_change > 0:
            print(f"  -> Creating new position for {symbol}")
            new_position = Position(symbol, quantity_change, price)
            self.add(new_position)
        else:
            print(f"  -> WARNING: Cannot sell {symbol}, position not held.")


    def __repr__(self):
        return f"PortfolioGroup(name='{self.name}', value={self.get_value():.2f}, items={len(self._children)})"