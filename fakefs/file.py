from typing import Optional

from node import Node

class File(Node):
    SYMBOL = 'f'

    def __init__(self, name: str, parent: Optional["Node"] = None):
        super().__init__(name, parent)
        self.content = ""    # Initially an empty file
        self.type_symbol = File.SYMBOL
