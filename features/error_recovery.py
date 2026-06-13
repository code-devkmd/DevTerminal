"""
Smart Error Recovery - Auto-suggests corrections for typos
Uses fuzzy matching and common mistakes database
"""
import difflib
from typing import Optional, List
from rich.console import Console
from rich.prompt import Confirm

console = Console()

# Common command typos mapping
COMMON_TYPOS = {
    # Git typos
    "git psuh": "git push",
    "git pull": "git pull",
    "git statsu": "git status",
    "git comit": "git commit",
    "git checkotu": "git checkout",
    "git branc": "git branch",
    "git clon": "git clone",
    "gut": "git",
    "gti": "git",
    
    # Docker typos
    "dokcer": "docker",
    "docker-comopse": "docker-compose",
    "docker sp": "docker ps",
    
    # Common commands
    "cd..": "cd ..",
    "claer": "clear",
    "celar": "clear",
    "exti": "exit",
    "pyhton": "python",
    "pythno": "python",
    "pip isntall": "pip install",
    "npm isntall": "npm install",
    "npm rnu": "npm run",
    "mkdri": "mkdir",
    "toch": "touch",
}

# All valid commands (will be populated from system)
VALID_COMMANDS = [
    "ls", "cd", "pwd", "cat", "mkdir", "rm", "cp", "mv", "touch",
    "git", "docker", "npm", "pip", "python", "node", "make",
    "grep", "find", "chmod", "chown", "curl", "wget", "ssh",
    "vim", "nano", "code", "clear", "exit", "echo", "kill"
]


class ErrorRecovery:
    """Handles command error detection and auto-correction"""
    
    def __init__(self):
        self.suggestion_threshold = 0.6
        self.max_suggestions = 3
    
    def check_typo(self, command: str, full_line: str) -> Optional[str]:
        """
        Check if command is a typo and suggest correction
        Returns: suggested command if found, None otherwise
        """
        # Check exact matches in common typos
        if full_line in COMMON_TYPOS:
            return COMMON_TYPOS[full_line]
        
        # Check command-only typos
        if command in COMMON_TYPOS:
            return COMMON_TYPOS[command]
        
        # Fuzzy match against valid commands
        suggestions = difflib.get_close_matches(
            command,
            VALID_COMMANDS,
            n=self.max_suggestions,
            cutoff=self.suggestion_threshold
        )
        
        if suggestions:
            return suggestions[0]
        
        return None
    
    def suggest_correction(self, wrong_cmd: str, full_line: str) -> Optional[str]:
        """
        Display suggestion and get user confirmation
        Returns: corrected command if accepted, None if rejected
        """
        suggestion = self.check_typo(wrong_cmd, full_line)
        
        if not suggestion:
            return None
        
        # Display suggestion
        console.print(f"[red]✗ Command not found:[/red] {wrong_cmd}")
        console.print(f"[yellow]💡 Did you mean:[/yellow] [green]{suggestion}[/green]")
        
        # Ask for confirmation (with timeout)
        try:
            if Confirm.ask("Run this command?", default=True):
                # Replace the wrong command with suggestion
                if full_line.strip() == wrong_cmd:
                    return suggestion
                else:
                    # Replace first occurrence in full line
                    return full_line.replace(wrong_cmd, suggestion, 1)
        except KeyboardInterrupt:
            console.print("[dim]Cancelled[/dim]")
            return None
        
        return None
    
    def get_multiple_suggestions(self, command: str) -> List[str]:
        """Get multiple suggestions for a command"""
        suggestions = difflib.get_close_matches(
            command,
            VALID_COMMANDS,
            n=self.max_suggestions,
            cutoff=0.5  # Lower threshold for multiple suggestions
        )
        return suggestions


# Global instance
error_recovery = ErrorRecovery()


def handle_command_not_found(command: str, full_line: str) -> Optional[str]:
    """
    Handle command not found error with smart suggestions
    Returns corrected command or None
    """
    return error_recovery.suggest_correction(command, full_line)