try:
    from patterns.singleton import config_manager
    from patterns.factory import InstrumentFactory
    from patterns.builder import PortfolioBuilder
    from patterns.strategy import MeanReversionStrategy, BreakoutStrategy
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file ./patterns. Error:{e}')
try:
    from analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file analytics.py. Error:{e}')
try:
    from data_loader import MarketDataPoint, YahooFinanceAdapter, CSVMarketDataAdapter
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file data_loader.py. Error:{e}')
try:
    from reporting import LoggerObserver, AlertObserver
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file reporting.py. Error:{e}')
try:
    from engine import TradingEngine
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file engine.py. Error:{e}')
try:
    from models import Instrument
except ModuleNotFoundError as e:
    print(f'Fatal! Source Broken. Please check source file models.py. Error:{e}')
import csv
import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("Initializing with Creational Patterns...")
    config_path = os.path.join(BASE_DIR, 'data','config.json')
    config_manager.load(config_path)
    instruments: dict[str, Instrument] = {}
    instruments_path = os.path.join(BASE_DIR,'data', 'instruments.csv')
    with open(instruments_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            instrument = InstrumentFactory.create_instrument(row)
            instruments[instrument.symbol] = instrument
    print(f"Factory created {len(instruments)} instruments.")

    portfolio_path = os.path.join(BASE_DIR,'data', 'portfolio_structure.json')
    with open(portfolio_path, 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    main_portfolio = PortfolioBuilder.build_from_dict(portfolio_data)
    print(f"Builder created portfolio '{main_portfolio.name}' with value ${main_portfolio.get_value():.2f}")
    print("Applying Structural Patterns...")

    aapl_stock = instruments.get('AAPL')
    if aapl_stock:
        decorated_aapl = DrawdownDecorator(BetaDecorator(VolatilityDecorator(aapl_stock)))
        print(f"Decorated metrics for AAPL: {decorated_aapl.get_metrics()}")

    yahoo_adapter_path = os.path.join(BASE_DIR,'data','external_data_yahoo.json')
    yahoo_adapter = YahooFinanceAdapter(yahoo_adapter_path)
    yahoo_data = yahoo_adapter.get_data()
    print(f"Adapter loaded data from Yahoo JSON: {yahoo_data}")

    print("Setting up Behavioral Patterns...")

    strategy_params_path = os.path.join(BASE_DIR, 'data','strategy_params.json')
    with open(strategy_params_path, 'r', encoding='utf-8') as f:
        strategy_params = json.load(f)
    strategy_name = config_manager.get('default_strategy', 'MeanReversionStrategy')
    params = strategy_params.get(strategy_name)
    if not params:
        raise ValueError(f"Parameters for strategy '{strategy_name}' not found.")

    active_strategy = MeanReversionStrategy(**params)

    logger = LoggerObserver()
    alerter = AlertObserver()

    engine = TradingEngine(strategy=active_strategy, portfolio=main_portfolio)
    engine.attach(logger)
    engine.attach(alerter)
    print("Trading engine is configured with 'Next Tick Execution' model.")

    print("Running Simulation...")

    csv_adapter_path = os.path.join(BASE_DIR, 'data','market_data.csv')
    csv_adapter = CSVMarketDataAdapter(csv_adapter_path)
    market_data_ticks = csv_adapter.get_data()
    print(f"Adapter loaded {len(market_data_ticks)} ticks from market_data.csv for simulation.")

    if not market_data_ticks:
        print("WARNING: No market data found from CSV. Simulation cannot run.")
        return

    print(f"Portfolio value BEFORE simulation: ${main_portfolio.get_value():.2f}")
    for tick in market_data_ticks:
        engine.process_tick(tick)

    if market_data_ticks:
        print("Flushing last pending order...")
        last_price = market_data_ticks[-1].price
        last_symbol = market_data_ticks[-1].symbol
        final_tick = MarketDataPoint(last_symbol, last_price + 0.01, 'T_END')
        engine.process_tick(final_tick)

    print(f"Portfolio value AFTER simulation: ${main_portfolio.get_value():.2f}")

    print("Testing Undo Functionality...")
    engine.undo_last_trade()

    print(f"Portfolio value AFTER undo: ${main_portfolio.get_value():.2f}")
    print("Simulation Finished.")


if __name__ == "__main__":
    main()