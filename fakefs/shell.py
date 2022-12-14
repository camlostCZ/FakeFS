from typing import Any

from fake_filesystem import Filesystem, FilesystemError
from cmd_handlers import (
    handle_cat, handle_cd, handle_edit, handle_help, handle_invalid_cmd,
    handle_ls, handle_mkdir, handle_rm, handle_touch
)

COMMANDS = {
    "exit": None,
    "help": handle_help,
    "ls": handle_ls,
    "mkdir": handle_mkdir,
    "rm": handle_rm,
    "touch": handle_touch,
    "cd": handle_cd,
    "cat": handle_cat,
    "edit": handle_edit
}


def parse_cmd(txt: str) -> tuple[str, Any]:
    result = (None, None)
    cmd = txt.strip().split(" ")[0].lower()
    if cmd in COMMANDS:
        result = (cmd, COMMANDS[cmd])
    return result


def update_prompt(fs: Filesystem) -> str:
    result = f"{fs.curdir.abs_path}> "
    return result


def main():
    fs = Filesystem("fake_01")

    finished = False
    while not finished:
        prompt = update_prompt(fs)
        text = input(prompt)
        cmd = parse_cmd(text)

        match cmd:
            case (None, _): handle_invalid_cmd(text)
            case ("exit", _): finished = True
            case (_, cmd_handler): cmd_handler(fs, text)
        # /match
    # /while


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by the user. Exiting.")
