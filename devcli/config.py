"""
Configuration File - Easy customization for team members
All settings in one place for better collaboration
"""
import os
from pathlib import Path

# ============================================================================
# TERMINAL SETTINGS
# ============================================================================

# Terminal Info
APP_NAME = "DevTerminal"
APP_VERSION = "2.0.0"
ENGINE_NAME = "DevCLI Core"

# Display Settings
SHOW_BANNER = True  # Set to False to skip banner
SHOW_GIT_BRANCH = True  # Show git branch in prompt
COMPRESS_HOME_DIR = True  # Show ~ instead of full home path

# ============================================================================
# PROMPT CUSTOMIZATION
# ============================================================================

# Prompt Colors (HTML color names or ANSI codes)
PROMPT_USER_COLOR = "ansigreen"  # User@host color
PROMPT_PATH_COLOR = "ansiblue"   # Current directory color
PROMPT_GIT_COLOR = "cyan"        # Git branch color

# Prompt Symbol
PROMPT_SYMBOL_UNIX = "$"
PROMPT_SYMBOL_WINDOWS = ">"

# ============================================================================
# COMMAND ALIASES (Team-wide shortcuts)
# ============================================================================

# Git shortcuts
GIT_ALIASES = {
    "gs": ["git", "status"],
    "ga": ["git", "add", "."],
    "gc": ["git", "commit", "-m"],
    "gp": ["git", "push"],
    "gl": ["git", "log", "--oneline"],
    "gd": ["git", "diff"],
}

# List shortcuts
LIST_ALIASES = {
    "ll": ["ls", "-al"],
    "la": ["ls", "-a"],
}

# Combine all aliases
COMMAND_ALIASES = {**GIT_ALIASES, **LIST_ALIASES}

# ============================================================================
# AUTO-COMPLETION SETTINGS
# ============================================================================

# Complete while typing (True = slower but more helpful)
COMPLETE_WHILE_TYPING = False

# Fuzzy matching threshold (0.0 - 1.0, lower = more lenient)
FUZZY_MATCH_CUTOFF = 0.4

# Number of suggestions to show
MAX_SUGGESTIONS = 5

# ============================================================================
# HISTORY SETTINGS
# ============================================================================

# History file location
HISTORY_DIR = Path.home() / ".devterminal"
HISTORY_FILE = HISTORY_DIR / "history"

# Create history directory if it doesn't exist
HISTORY_DIR.mkdir(exist_ok=True)

# Maximum history entries
MAX_HISTORY_SIZE = 1000

# ============================================================================
# COMMON FOLDERS (for auto-completion metadata)
# ============================================================================

FOLDER_DESCRIPTIONS = {
    'src': 'Source code',
    'bin': 'Binaries',
    'doc': 'Documentation',
    'test': 'Tests',
    'lib': 'Libraries',
    'config': 'Configuration',
    'dist': 'Distribution',
    'build': 'Build output',
    'node_modules': 'Node dependencies',
    'venv': 'Virtual environment',
    '.git': 'Git repository',
}

# ============================================================================
# PLATFORM DETECTION
# ============================================================================

IS_WINDOWS = os.name == "nt"
IS_LINUX = os.name == "posix" and os.uname().sysname == "Linux"
IS_MAC = os.name == "posix" and os.uname().sysname == "Darwin"

# ============================================================================
# DEVELOPER NOTES
# ============================================================================

"""
TEAM COLLABORATION TIPS:

1. To add new aliases:
   - Add them to COMMAND_ALIASES dictionary above
   - Format: "shortcut": ["full", "command", "with", "args"]

2. To change colors:
   - Modify PROMPT_*_COLOR variables
   - Use HTML color names or ANSI codes

3. To add folder descriptions:
   - Add entries to FOLDER_DESCRIPTIONS dictionary
   - These appear as hints during auto-completion

4. To disable features:
   - Set SHOW_BANNER = False to skip startup banner
   - Set SHOW_GIT_BRANCH = False to hide git info
   - Set COMPLETE_WHILE_TYPING = False for faster typing

5. For testing:
   - Change APP_VERSION when releasing
   - Modify MAX_HISTORY_SIZE if history grows too large
"""