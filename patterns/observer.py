from __future__ import annotations
from typing import List, Dict
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self,signal:Dict):
        pass

class SignalPublisher():
    """Notify observers, stores data of observers"""
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self,observer:Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self,observer:Observer):
        self._observers.remove(observer)

    def notify(self,signal:Dict):
        for observer in self._observers:
            observer.update(signal)

