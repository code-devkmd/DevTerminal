import os
import difflib

def check_path_and_suggest(path):
    """
    Checks if a path exists. If not, provides fuzzy-matched suggestions.
    Returns: (is_valid: bool, suggestions: list)
    """
    if os.path.exists(path):
        return True, []

    dirname = os.path.dirname(path) or '.'
    basename = os.path.basename(path)

    if os.path.isdir(dirname):
        items = os.listdir(dirname)
        # Fuzzy match the file/folder name
        suggestions = difflib.get_close_matches(basename, items, n=3, cutoff=0.5)
        
        if suggestions:
            # Reconstruct the path if a directory was specified
            if dirname != '.':
                suggestions = [os.path.join(dirname, s) for s in suggestions]
            return False, suggestions
            
    return False, []