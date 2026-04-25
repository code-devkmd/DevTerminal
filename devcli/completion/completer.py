import os
import difflib
import platform
from devcli.os_layer.commands import COMMANDS
from prompt_toolkit.completion import Completer, Completion

SEPARATOR = os.sep

COMMON_FOLDERS = {
    'src': 'Source code',
    'bin': 'Binaries',
    'doc': 'Documents'
}

class DevTerminalCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()

        # 1. Command Auto-completion
        if not words or (len(words) == 1 and not text.endswith(' ')):
            word = words[0].lower() if words else ''
            for cmd in COMMANDS:
                if cmd.startswith(word):
                    yield Completion(cmd, start_position=-len(word))
            return

        # 2. File/Directory Auto-completion
        last_word = words[-1] if not text.endswith(' ') else ''
        dirname = os.path.dirname(last_word) or '.'
        basename = os.path.basename(last_word)

        if os.path.isdir(dirname):
            items = os.listdir(dirname)
            
            # Case-insensitive prefix match for Windows
            base = basename.lower()
            matches = [i for i in items if i.lower().startswith(base)]            
            # Fuzzy match fallback
            if not matches and basename:
                matches = difflib.get_close_matches(basename, items, n=5, cutoff=0.4)

            for match in matches:
                display_meta = COMMON_FOLDERS.get(match.lower(), "")
                
                full_path = os.path.join(dirname, match)
                if os.path.isdir(full_path):
                    match += SEPARATOR
                    
                yield Completion(
                    match, 
                    start_position=-len(basename),
                    display_meta=display_meta
                )