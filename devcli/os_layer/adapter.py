from .commands import COMMAND_MAP
from .detector import IS_WINDOWS
from rich.prompt import Confirm

SAFE_COMMANDS = ["ls", "pwd", "cd", "ll", "gs"]

# Global Developer Aliases (Cross-platform)
DEV_ALIASES = {
    "gs": ["git", "status"],
    "ga": ["git", "add", "."],
    "gc": ["git", "commit", "-m"],
    "ll": ["ls", "-al"] if not IS_WINDOWS else ["dir"]
}

def adapt_command(cmd, args):
    # 1. Expand Developer Aliases
    if cmd in DEV_ALIASES:
        expanded = DEV_ALIASES[cmd]
        cmd = expanded[0]
        args = expanded[1:] + args
        return cmd, args, True

    # 2. OS Translation (Linux -> Windows)
    if IS_WINDOWS and cmd in COMMAND_MAP:
        mapped = COMMAND_MAP[cmd]

        if cmd in SAFE_COMMANDS:
            return mapped, args, True

        if Confirm.ask(f"Convert '{cmd}' → '{mapped}'?"):
            return mapped, args, True
        else:
            return cmd, args, False

    return cmd, args, True