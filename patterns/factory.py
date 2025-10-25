try:
    from models import Instrument, Stock, Bond, ETF
except ModuleNotFoundError:
    print("Fatal! Source Broken. Please implement source models.py under ./patterns")
from typing import Dict

class InstrumentFactory:
    #registry
    _creators = {
        'Stock':Stock,
        'Bond':Bond,
        'ETF':ETF
    }
    @classmethod
    def register_instrument(cls,instrument_type: str,creator):
        cls._creators[instrument_type] =creator

    @classmethod
    def create_instrument(cls,data:Dict)->Instrument:
        """
        Robust Unpackaging
        """
        instrument_type = data.get('type')
        if not instrument_type:
            raise ValueError("Data dictionary must contain a 'type' key.")
        creator = cls._creators.get(instrument_type)
        if not creator:
            raise ValueError(f"Unknown instrument type: {instrument_type}")
        constructor_args = data.copy()
        ##fix1 by Yuting
        # if 'name' not in constructor_args:
        #     constructor_args['name'] = constructor_args.get('type', 'UNKNOWN')
        symbol = constructor_args.get('symbol')
        name = constructor_args.get('type')

        return creator(symbol=symbol,name=name)