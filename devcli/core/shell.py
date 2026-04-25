import os
import getpass
import platform
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer

from devcli.completion.completer import DevTerminalCompleter
from devcli.completion.suggester import DevAutoSuggest
from devcli.core.history import get_history
from .executor import execute_command

kb = KeyBindings()

@kb.add("right")
def _(event):
    buffer = event.app.current_buffer
    if buffer.suggestion:
        buffer.insert_text(buffer.suggestion.text)

def get_git_branch():
    """Silently fetches the current git branch if in a repository."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'], 
            capture_output=True, 
            text=True, 
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0 and result.stdout.strip():
            return f" git:(<ansired>{result.stdout.strip()}</ansired>)"
    except Exception:
        pass
    return ""

def get_prompt():
    user = getpass.getuser()
    host = platform.node()
    cwd = os.getcwd()

    # Compress home directory
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]

    symbol = "$" if os.name != "nt" else ">"
    git_info = get_git_branch()

    return HTML(
        f"<ansigreen>{user}@{host}</ansigreen>:"
        f"<ansiblue>{cwd}</ansiblue>{git_info}{symbol} "
    )

def run_shell():
    # We initialize the PygmentsLexer with BashLexer to handle standard shell syntax
    session = PromptSession(
        completer=DevTerminalCompleter(),
        history=get_history(),
        complete_while_typing=False,
        auto_suggest=DevAutoSuggest(),
        lexer=PygmentsLexer(BashLexer),  
        key_bindings=kb
    )

    while True:
        try:
            command = session.prompt(get_prompt())
            if not execute_command(command):
                break
        except KeyboardInterrupt:
            continue
        except EOFError:
            break