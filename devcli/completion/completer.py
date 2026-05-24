"""
Auto-Completer - Intelligent command and path completion
Optimized for speed and accuracy
"""
import os
import difflib
from typing import Iterable
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

from devcli.os_layer.commands import COMMANDS

# Import configuration
try:
    from devcli.config import FOLDER_DESCRIPTIONS, FUZZY_MATCH_CUTOFF, MAX_SUGGESTIONS
except ImportError:
    FOLDER_DESCRIPTIONS = {'src': 'Source code', 'bin': 'Binaries', 'doc': 'Documents'}
    FUZZY_MATCH_CUTOFF = 0.4
    MAX_SUGGESTIONS = 5

SEPARATOR = os.sep

class DevTerminalCompleter(Completer):
    """Smart completer with command and path completion"""
    
    def get_completions(
        self, 
        document: Document, 
        complete_event
    ) -> Iterable[Completion]:
        """Generate completions based on current input"""
        text = document.text_before_cursor
        words = text.split()
        
        # Command completion (first word)
        if not words or (len(words) == 1 and not text.endswith(' ')):
            yield from self._complete_command(words)
            return
        
        # Path/File completion (subsequent words)
        yield from self._complete_path(words, text)
    
    def _complete_command(self, words) -> Iterable[Completion]:
        """Complete command names"""
        word = words[0].lower() if words else ''
        
        for cmd in COMMANDS:
            if cmd.startswith(word):
                yield Completion(
                    cmd, 
                    start_position=-len(word),
                    display_meta="command"
                )
    
    def _complete_path(self, words, text) -> Iterable[Completion]:
        """Complete file and directory paths"""
        # Get the last word (might be partial path)
        last_word = words[-1] if not text.endswith(' ') else ''
        
        # Split into directory and basename
        dirname = os.path.dirname(last_word) or '.'
        basename = os.path.basename(last_word)
        
        # Check if directory exists
        if not os.path.isdir(dirname):
            return
        
        try:
            items = os.listdir(dirname)
        except (PermissionError, OSError):
            return
        
        # Find matches
        matches = self._find_matches(basename, items)
        
        # Generate completions
        for match in matches[:MAX_SUGGESTIONS]:
            full_path = os.path.join(dirname, match)
            
            # Add separator for directories
            display = match
            if os.path.isdir(full_path):
                display += SEPARATOR
            
            # Get metadata
            meta = self._get_metadata(match, full_path)
            
            yield Completion(
                display,
                start_position=-len(basename),
                display_meta=meta
            )
    
    def _find_matches(self, prefix: str, items: list) -> list:
        """Find matching items with fuzzy fallback"""
        # Case-insensitive prefix match (primary)
        prefix_lower = prefix.lower()
        matches = [i for i in items if i.lower().startswith(prefix_lower)]
        
        # Fuzzy match fallback if no prefix matches
        if not matches and prefix:
            matches = difflib.get_close_matches(
                prefix, 
                items, 
                n=MAX_SUGGESTIONS, 
                cutoff=FUZZY_MATCH_CUTOFF
            )
        
        return matches
    
    def _get_metadata(self, name: str, full_path: str) -> str:
        """Get descriptive metadata for completion"""
        # Check if it's a known folder type
        name_lower = name.lower()
        if name_lower in FOLDER_DESCRIPTIONS:
            return FOLDER_DESCRIPTIONS[name_lower]
        
        # Generic metadata
        if os.path.isdir(full_path):
            return "directory"
        elif os.path.isfile(full_path):
            # Get file extension
            _, ext = os.path.splitext(name)
            if ext:
                return f"{ext[1:]} file"
            return "file"
        
        return ""