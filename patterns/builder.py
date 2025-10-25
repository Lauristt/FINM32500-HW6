from __future__ import annotations
from typing import Dict, Any
try:
    from models import PortfolioGroup, Position
except ModuleNotFoundError:
    print("Fatal! Source Broken. Please implement source models.py under ./patterns")

class PortfolioBuilder():
    """
    Build portfolio using models.py -> PortfolioGroup()
    """
    def __init__(self,name:str):
        self._portfolio = PortfolioGroup(name)
    def set_owner(self,owner:str) -> PortfolioBuilder:
        self._portfolio.owner = owner
        return self
    def add_position(self,symbol: str,price:float,quantity:int) -> PortfolioBuilder:
        self._portfolio.add(Position(symbol,quantity,price))
        return self
    def add_sub_portfolio(self,sub_portfolio:PortfolioGroup) -> PortfolioBuilder:
        """
        PortfolioGroup inherits from PortfolioComponent
        Adds sub_portfolio to the original portfolio
        """
        self._portfolio.add(sub_portfolio)
        return self
    def build(self) -> PortfolioGroup:
        return self._portfolio

    @staticmethod
    def build_from_dict(data: Dict[str, Any]) -> PortfolioGroup:
        """
        Build PortfolioGroup from json
        :param data: Dict[str, Any]
        :return: PortfolioGroup
        """
        if 'name' not in data:
            raise ValueError("Portfolio data must contain a 'name'.")
        builder = PortfolioBuilder(data['name'])
        if 'owner' in data:
            builder.set_owner(data['owner'])
        for pos_data in data.get('positions', []):
            builder.add_position(
                pos_data['symbol'], pos_data['quantity'], pos_data['price']
            )
        for sub_data in data.get('sub_portfolios', []):
            sub_portfolio = PortfolioBuilder.build_from_dict(sub_data)
            builder.add_sub_portfolio(sub_portfolio)

        return builder.build()
