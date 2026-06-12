"""
Shell Interface - Main interactive loop
Uses configuration for easy customization
"""
import os
import getpass
import platform
import subprocess
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer

from devcli.completion.completer import DevTerminalCompleter
from devcli.completion.suggester import DevAutoSuggest
from devcli.core.history import get_history
from devcli.core.executor import execute_command

# Import configuration
try:
    from devcli.config import (
        SHOW_GIT_BRANCH, COMPRESS_HOME_DIR, 
        PROMPT_USER_COLOR, PROMPT_PATH_COLOR, PROMPT_GIT_COLOR,
        PROMPT_SYMBOL_UNIX, PROMPT_SYMBOL_WINDOWS,
        COMPLETE_WHILE_TYPING
    )
except ImportError:
    # Fallback defaults if config not found
    SHOW_GIT_BRANCH = True
    COMPRESS_HOME_DIR = True
    PROMPT_USER_COLOR = "ansigreen"
    PROMPT_PATH_COLOR = "ansiblue"
    PROMPT_GIT_COLOR = "cyan"
    PROMPT_SYMBOL_UNIX = "$"
    PROMPT_SYMBOL_WINDOWS = ">"
    COMPLETE_WHILE_TYPING = False

# Key bindings
kb = KeyBindings()

@kb.add("c-v")
def _(event):
    event.current_buffer.paste_clipboard_data(
        event.app.clipboard.get_data()
    )

@kb.add("right")
def accept_suggestion(event):
    """Accept auto-suggestion with right arrow"""
    buffer = event.app.current_buffer
    if buffer.suggestion:
        buffer.insert_text(buffer.suggestion.text)

def get_git_branch() -> str:
    """Get current git branch if in a git repository"""
    if not SHOW_GIT_BRANCH:
        return ""
    
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=1  # Prevent hanging
        )
        
        if result.returncode == 0 and result.stdout.strip():
            branch = result.stdout.strip()
            return f" (<{PROMPT_GIT_COLOR}>{branch}</{PROMPT_GIT_COLOR}>)"
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    
    return ""

def get_prompt() -> HTML:
    """Generate dynamic prompt with user@host:path format"""
    user = getpass.getuser()
    host = platform.node()
    cwd = os.getcwd()
    
    # Compress home directory to ~
    if COMPRESS_HOME_DIR:
        home = os.path.expanduser("~")
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
    
    # Choose symbol based on OS
    symbol = PROMPT_SYMBOL_WINDOWS if os.name == "nt" else PROMPT_SYMBOL_UNIX
    
    # Get git branch info
    git_info = get_git_branch()
    
    return HTML(
        f"<{PROMPT_USER_COLOR}>{user}@{host}</{PROMPT_USER_COLOR}>:"
        f"<{PROMPT_PATH_COLOR}>{cwd}</{PROMPT_PATH_COLOR}>"
        f"{git_info}{symbol} "
    )

def run_shell():
    """Main interactive shell loop"""
    session = PromptSession(
        completer=DevTerminalCompleter(),
        history=get_history(),
        complete_while_typing=COMPLETE_WHILE_TYPING,
        auto_suggest=DevAutoSuggest(),
        lexer=PygmentsLexer(BashLexer),
        clipboard=PyperclipClipboard(),
        key_bindings=kb
    )
    
    while True:
        try:
            command = session.prompt(get_prompt())
            
            # Execute command and check if should continue
            if not execute_command(command):
                break
                
        except KeyboardInterrupt:
            # Ctrl+C just cancels current line
            continue
            
        except EOFError:
            # Ctrl+D exits shell
            break