import os
import subprocess
import shlex
from rich.console import Console
from devcli.os_layer.adapter import adapt_command

console = Console()

# Track previous directory for `cd -` functionality
PREVIOUS_DIR = os.getcwd()

def execute_command(command_line):
    global PREVIOUS_DIR
    if not command_line.strip():
        return True

    # Expand environment variables ($VAR or %VAR%)
    command_line = os.path.expandvars(command_line)
    is_windows = os.name == "nt"

    try:
        parts = shlex.split(command_line, posix=not is_windows)
    except ValueError as e:
        console.print(f"[red]Parse error: {e}[/red]")
        return True

    if not parts:
        return True

    cmd = parts[0]
    args = parts[1:]

    cmd, args, proceed = adapt_command(cmd, args)
    if not proceed:
        return True

    # Smart handling
    if cmd == "type" and args:
        target = args[0]
        if os.path.isdir(target):
            console.print("[yellow]Detected directory → using 'dir' instead[/yellow]")
            cmd = "dir"
            args = [target]

    # --- Built-ins ---
    if cmd == "exit":
        return False

    if cmd in ["clear", "cls"]:
        os.system("cls" if is_windows else "clear")
        return True

    if cmd == "cd":
        current_dir = os.getcwd()
        
        # Handle `cd -` (go to previous directory)
        if args and args[0] == "-":
            target = PREVIOUS_DIR
            console.print(f"[dim]{target}[/dim]")
        else:
            target = args[0] if args else os.path.expanduser("~")

        if os.path.isdir(target):
            os.chdir(target)
            PREVIOUS_DIR = current_dir # Save state for next `cd -`
        else:
            console.print(f"[red]Not a directory:[/red] {target}")
        return True

    # --- Execution ---
    try:
        if is_windows:
            # shell=True is mandatory on Windows for built-ins like 'dir'
            full_cmd = f"{cmd} {' '.join(args)}"
            subprocess.run(full_cmd, shell=True)
        else:
            subprocess.run([cmd] + args)
    except FileNotFoundError:
        console.print(f"[red]Command not found:[/red] {cmd}")
    except Exception as e:
        console.print(f"[red]Execution error:[/red] {e}")

    return True