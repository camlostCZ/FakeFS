from typing import Optional

from file import File
from filesystemerror import FilesystemError
from folder import Folder
from node import Node


class Filesystem(Folder):
    """
    A filesystem - a root container of Filenodes.
    """

    SEPARATOR = '/'
    SYMBOL = '#'

    def __init__(self, name: str, path_separator: str = SEPARATOR):
        self.curdir = self
        super().__init__(name)
        self.type_symbol = Filesystem.SYMBOL
        self.path_separator = path_separator

    def add_folder(self, name: str):
        self.curdir._add_node(Folder(name))

    def add_file(self, name: str):
        self.curdir._add_node(File(name))

    def change_curdir(self, path: str):
        cd = self.search_folder(path)
        if cd:
            self.curdir = cd

    def get_node_path(self, node: Node) -> str:
        """
        Get node path (using the path_separator).

        Args:
            node (Node): Node to get path to.

        Returns:
            str: Path from root to the node.
        """
        result = ""
        nodes = []
        while node.parent is not None:
            nodes.insert(0, node.name)
            node = node.parent
        result = self.path_separator + self.path_separator.join(nodes)
        return result

    def remove_file(self, name: str):
        node = self.curdir.nodes.get(name)
        if node is not None and node.type_symbol == File.SYMBOL:
            self.curdir._remove_node(node)
        else:
            raise FilesystemError(f"File '{name}' not found.")

    def search_folder(self, path: str) -> Optional[Folder]:
        """
        Search for folder by path.

        Args:
            path (str): Path to a folder.

        Raises:
            FilesystemError: If non-existing path detectd.

        Returns:
            Optional[Folder]: Folder if found at the path, None otherwise.
        """
        result = None
        if path:
            cd = self if path[0] == self.path_separator else self.curdir
            path_names = path.split(self.path_separator)
            for name in path_names:
                if name == "" or name == ".":  # Skip
                    continue
                if name == "..":  # Go up
                    if cd.parent:
                        cd = cd.parent
                    else:
                        raise FilesystemError(f"Invalid path '{path}'.")
                else:  # Go down
                    cd = cd.nodes.get(name)
                    if not cd or cd.type_symbol != Folder.SYMBOL:
                        raise FilesystemError(f"'{name}' is not a folder in '{path}'.")
            result = cd
        return result

    def search_file(self, path: str) -> Optional[File]:
        result = None
        cwd = self.curdir
        idx = path.rfind(self.path_separator)
        if idx > -1:
            cwd = self.search_folder(path[:idx])
        node = cwd.nodes.get(path[idx + 1:])
        if node and node.type_symbol == File.SYMBOL:
            result = node
        else:
            raise FilesystemError(f"File '{path}' not found.")
        return result
