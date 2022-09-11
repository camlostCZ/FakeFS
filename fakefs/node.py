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
        self.abs_path = ""
        self.update_abspath()

    def update_abspath(self, sep: str):
        """
        Update node `abs_path` using a separator.

        Args:
            sep (str): Path separator ('/' usually)
        """
        if self.parent is not None:
            self.abs_path = sep.join([self.parent.abs_path, self.name])
        else:
            self.abs_path = f"{sep}{self.name}"
