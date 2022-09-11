from typing import Optional

from file import File
from filesystemerror import FilesystemError
from folder import Folder


class Filesystem(Folder):
    """
    A filesystem - a root container of Filenodes.
    """

    SEPARATOR = '/'
    SYMBOL = '/'

    def __init__(self, name: str):
        self.curdir = self
        super().__init__(name)
        self.type_symbol = Filesystem.SYMBOL

    def add_folder(self, name: str):
        self.curdir._add_node(Folder(name))

    def add_file(self, name: str):
        self.curdir._add_node(File(name))

    def change_curdir(self, path: str):
        cd = self.search_folder(path)
        if cd:
            self.curdir = cd

    def remove_file(self, name: str):
        node = self.curdir.nodes.get(name)
        if node is not None and node.type_symbol == File.SYMBOL:
            self.curdir._remove_node(node)
        else:
            raise FilesystemError(f"File '{name}' not found.")

    def search_folder(self, path: str) -> Optional[Folder]:
        result = None
        if path:
            cd = self if path[0] == Filesystem.SEPARATOR else self.curdir
            path_names = path.split(Filesystem.SEPARATOR)
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
        idx = path.rfind(Filesystem.SEPARATOR)
        if idx > -1:
            cwd = self.search_folder(path[:idx])
        node = cwd.nodes.get(path[idx + 1:])
        if node and node.type_symbol == File.SYMBOL:
            result = node
        else:
            raise FilesystemError(f"File '{path}' not found.")
        return result
