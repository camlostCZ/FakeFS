from typing import Optional

from filesystemerror import FilesystemError
from node import Node

class Folder(Node):
    SYMBOL = 'd'

    def __init__(self, name: str, parent: Optional["Node"] = None):
        super().__init__(name, parent)
        self.nodes: dict[str, Node] = {}
        self.type_symbol = Folder.SYMBOL

    def _add_node(self, node: Node):
        if node.name in self.nodes.keys():
            raise FilesystemError(f"Node with the same name {node.name} already exists.")
        else:
            self.nodes[node.name] = node
            node.parent = self

    def _remove_node(self, node: Node):
        self.nodes.pop(node.name)
