from prompt_toolkit.history import FileHistory
import os

HISTORY_FILE = os.path.expanduser("~/.devterminal_history")

def get_history():
	return FileHistory(HISTORY_FILE)