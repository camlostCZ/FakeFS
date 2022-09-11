import datetime

from typing import Optional

class Node:
    """
    Filesystem node, i.e. a folder or a file or other type of node.
    """

    def __init__(self, name: str, type_symbol: str, parent: Optional["Node"] = None):
        self.name = name
        self.parent = parent
        self.type_symbol = type_symbol
        self.when_created = datetime.datetime.now()
