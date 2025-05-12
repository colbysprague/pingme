# notifier.py
# An interface for adding other clients to be notified by. 

from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass
