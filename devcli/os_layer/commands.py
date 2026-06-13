from .detector import IS_WINDOWS

if IS_WINDOWS:
    COMMANDS = [
        "cd", "dir", "type", "cls", "del", "mkdir", "rmdir", "exit"
    ]

    COMMAND_MAP = {
        "ls": "dir",
        "cat": "type",
        "rm": "del",
        "clear": "cls",
        "pwd": "cd"
    }

else:
    COMMANDS = [
        "cd", "ls", "cat", "clear", "rm", "mkdir", "pwd", "exit"
    ]

    COMMAND_MAP = {}  # No conversion needed