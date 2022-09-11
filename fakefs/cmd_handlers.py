import functools

from textwrap import dedent

from fake_filesystem import Filesystem, FilesystemError


def cmd_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        if len(args) == 2:
            parsed = args[1].strip().split(" ")
            if len(parsed) == 2:
                cmd, param = parsed
                try:
                    result = func(args[0], param, *args[2:], **kwargs)
                except FilesystemError as e:
                    print(f"Error: {e}")
            else:
                handle_invalid_cmd(args[1])
        else:
            result = func(*args, **kwargs)
        return result

    return wrapper


@cmd_handler
def handle_cat(fs: Filesystem, param: str):
    node = fs.search_file(param)
    if node:
        print(node.content)


@cmd_handler
def handle_cd(fs: Filesystem, param: str):
    fs.change_curdir(param)


@cmd_handler
def handle_edit(fs: Filesystem, param: str):
    node = fs.search_file(param)
    if node:
        print("Enter file content. Use '.' on the last line to finish input.")
        while (line := input()) != ".":
            node.content += line + "\n"


def handle_help(fs: Filesystem, txt: str):
    print("Known commands:")
    print(dedent("""
      Shell commands:
        exit         - exit shell
        help         - display this help

      Folder operations:
        cd <path>    - change current folder (aka directory)
        ls           - list current folder content
        mkdir <path> - create a new folder

      File operations:
        cat <path>   - print file content
        edit <path>  - set file content
        rm <path>    - remove a file
        touch <path> - create a new file
    """))


def handle_invalid_cmd(txt: str):
    print(f"Unknown command '{txt}'.\nSee help.")


def handle_ls(fs: Filesystem, cmd: str):
    data = []
    for n in sorted(fs.curdir.nodes.values(), key=lambda x: x.name):
        time_str = n.when_created.strftime("%Y-%m-%d %H:%M:%S")
        data.append(f"    [{n.type_symbol}]   {time_str}   {n.name}")

    print("    Type  Created               Name")
    print("\n".join(data))
    nodes_count = len(fs.curdir.nodes)
    print(f"{nodes_count} item(s) listed.")


@cmd_handler
def handle_mkdir(fs: Filesystem, param: str):
    fs.add_folder(param)


@cmd_handler
def handle_rm(fs: Filesystem, param: str):
    fs.remove_file(param)


@cmd_handler
def handle_touch(fs: Filesystem, param: str):
    fs.add_file(param)
