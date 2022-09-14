from re import T
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

    def get_node_tree(
            self,
            node: Node,
            level_sep: str,
            depth: int = 1) -> list[str]:
        """
        Get visual tree representation of node content.

        Args:
            node (Node): Node for which tree is generated
            level_sep (str): String used to indend level
            depth (int, optional): Tree level / depth. Defaults to 1.

        Returns:
            list[str]: List of (indented) node names visually representing
                a tree.
        """
        if depth >= 20:
            raise FilesystemError("Tree to deep.")

        result = []
        if node is not None:
            names = sorted(node.nodes.keys())
            for n in names:
                result.append(f"{level_sep * depth} {n}")
                if isinstance(node.nodes[n], Folder):
                    subtree = self.get_node_tree(node.nodes[n], level_sep, depth + 1)
                    result.extend(subtree)
        return result

    def remove_file(self, name: str):
        node = self.curdir.nodes.get(name)
        if isinstance(node, File):
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
                    if not isinstance(cd, Folder):
                        raise FilesystemError(f"'{name}' is not a folder in '{path}'.")
            result = cd
        return result

    def search_file(self, path: str) -> Optional[File]:
        result = None
        fld_path, filename = self.split_path(path)
        conditions = [
            filename is not None,
            (fld := self.search_folder(fld_path)) is not None,
            (result := fld.nodes.get(filename)) is not None,
            isinstance(result, File)
        ]
        if not all(conditions):
            raise FilesystemError(f"File '{path}' not found.")
        return result

    def search_parent(self, path: str) -> Optional[Folder]:
        result = None
        idx = path.rfind(self.path_separator)
        if idx > -1:
            result = self.search_folder(path[:idx])
        return result

    def split_path(self, path: str) -> tuple[str, str]:
        """
        Split path to folder path and filename.

        Args:
            path (str): Path to a node

        Returns:
            tuple[str, str]: Tuple of folder path, filename. Filename is an
                empty string if not found.
        """
        idx = path.rfind(self.path_separator)
        if idx > -1:
            fld_path = path[:idx]
            filename = path[idx + 1:]
        else:
            fld_path = path
            filename = ""
        # BUG Doesn't work for files in the root folder.
        return (fld_path, filename)
