from __future__ import annotations

from abc import ABC, abstractmethod

class UserInterface(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @abstractmethod
    def build_ui(self):
        pass