try:
    from models import Instrument
except ModuleNotFoundError:
    print("Fatal! Source Broken. Please implement source models.py under ./patterns")
from typing import Dict

class AnalyticsDecorator(Instrument):
    """An adapter class of standard 'Instrument' class"""
    _wrapped_instruments: Instrument = None

    def __init__(self,instrument: Instrument) -> None:
        self._wrapped_instruments = instrument

    def get_metrics(self) -> Dict:
        return self._wrapped_instruments.get_metrics()

    def __getattr__(self,name):
        return getattr(self._wrapped_instruments,name)

class VolatilityDecorator(AnalyticsDecorator):
    def get_metrics(self) -> Dict:
        metrics=super().get_metrics()
        metrics['volatility']=0.25
        # just put it here for future dev
        return metrics

class BetaDecorator(AnalyticsDecorator):
    def get_metrics(self) -> Dict:
        metrics = super().get_metrics()
        metrics['beta'] = 1.2 # same as above
        return metrics

class DrawdownDecorator(AnalyticsDecorator):
    def get_metrics(self) -> Dict:
        metrics = super().get_metrics()
        metrics['max_drawdown'] = 0.15 # same as above
        return metrics