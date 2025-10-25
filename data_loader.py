# write an adapter to convert any type of data into MarketDataPoint
import json
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict
from abc import abstractmethod

class MarketDataPoint:
    def __init__(self,symbol:str,price:float,timestamp:str,volume:int=0):
        self.symbol = symbol
        self.price = float(price)
        self.timestamp = timestamp
        self.volume = volume
    def __repr__(self):
        return (f"MarketDataPoint(symbol='{self.symbol}', price={self.price}, "
                f"timestamp='{self.timestamp}')")

@abstractmethod
class DataAdapter():
    def get_data(self)->List[MarketDataPoint]:
        pass

#Adapter for Yahoo Finance Json
class YahooFinanceAdapter(DataAdapter):
    """
    Convert Json downloaded from Yahoo finance to an MarketDataPoint
    """
    def __init__(self,file_path:str):
        self.file_path = file_path
    def get_data(self) -> List[MarketDataPoint]:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            if isinstance(data,dict):
                return [
                    MarketDataPoint(symbol = data['ticker'],
                                    price = float(data['last_price']),
                                    timestamp = data['timestamp']
                                    )]
            return []
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading or parsing Yahoo data from {self.file_path}: {e}")
            return []

class BloombergXMLAdapter(DataAdapter):
    """
    Convert Json downloaded from Bloomberg to an MarketDataPoint
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
    def get_data(self) -> List[MarketDataPoint]:
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            data_points = []
            for tick in root.findall('tick'):
                data_points.append(
                    MarketDataPoint(
                        symbol=tick.get('symbol'),
                        price=float(tick.get('price')),
                        timestamp=tick.get('ts')
                    )
                )
            return data_points
        except (IOError, ET.ParseError) as e:
            print(f"Error reading or parsing Bloomberg data from {self.file_path}: {e}")
            return []


class CSVMarketDataAdapter(DataAdapter):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_data(self) -> List[MarketDataPoint]:
        data_points = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data_points.append(
                        MarketDataPoint(
                            symbol=row['symbol'],
                            price=float(row['price']),
                            timestamp=row['timestamp']
                        )
                    )
        except (IOError, csv.Error, KeyError, ValueError) as e:
            print(f"Error reading or parsing CSV data from {self.file_path}: {e}")
            return []

        return data_points