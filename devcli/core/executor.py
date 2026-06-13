"""
Command Executor - Now with Smart Features!
Includes: Error Recovery, Port Manager, Project Switcher, HTTP Testing
"""
import os
import subprocess
import shlex
from typing import Tuple, List
from rich.console import Console
from devcli.os_layer.adapter import adapt_command

# Import new features
from devcli.features.error_recovery import handle_command_not_found
from devcli.features.port_manager import cmd_ports, cmd_kill_port
from devcli.features.project_switcher import cmd_proj
from devcli.features.http_tester import cmd_http, cmd_post, cmd_headers

console = Console()

class CommandExecutor:
    """Handles command execution with state management"""
    
    def __init__(self):
        self.previous_dir = os.getcwd()
        self.is_windows = os.name == "nt"
    
    def parse_command(self, command_line: str) -> Tuple[str, List[str]]:
        """Parse command line into command and arguments"""
        # Expand environment variables
        command_line = os.path.expandvars(command_line)
        
        try:
            parts = shlex.split(command_line, posix=not self.is_windows)
        except ValueError as e:
            console.print(f"[red]Parse error: {e}[/red]")
            return None, []
        
        if not parts:
            return None, []
        
        return parts[0], parts[1:]
    
    def handle_builtin(self, cmd: str, args: List[str]) -> Tuple[bool, bool, str]:
        """
        Handle built-in commands
        Returns: (is_builtin, should_continue, new_path)
        """
        # Exit command
        if cmd == "exit":
            return True, False, None
        
        # Clear screen
        if cmd in ["clear", "cls"]:
            os.system("cls" if self.is_windows else "clear")
            return True, True, None
        
        # Change directory
        if cmd == "cd":
            self._handle_cd(args)
            return True, True, None
        
        # NEW FEATURES!
        
        # Port manager
        if cmd == "ports":
            cmd_ports(args)
            return True, True, None
        
        if cmd == "kill-port":
            cmd_kill_port(args)
            return True, True, None
        
        # Project switcher
        if cmd == "proj":
            should_continue, new_path = cmd_proj(args)
            return True, should_continue, new_path
        
        # HTTP testing
        if cmd == "http":
            cmd_http(args)
            return True, True, None
        
        if cmd == "post":
            cmd_post(args)
            return True, True, None
        
        if cmd == "headers":
            cmd_headers(args)
            return True, True, None
        
        return False, True, None
    
    def _handle_cd(self, args: List[str]):
        """Handle cd command with history support"""
        current_dir = os.getcwd()
        
        # Handle `cd -` (go to previous directory)
        if args and args[0] == "-":
            target = self.previous_dir
            console.print(f"[dim]{target}[/dim]")
        else:
            target = args[0] if args else os.path.expanduser("~")
        
        if os.path.isdir(target):
            os.chdir(target)
            self.previous_dir = current_dir
        else:
            console.print(f"[red]Not a directory:[/red] {target}")
    
    def smart_type_handler(self, cmd: str, args: List[str]) -> Tuple[str, List[str]]:
        """Smart handling for 'type' command on Windows"""
        if cmd == "type" and args and self.is_windows:
            target = args[0]
            if os.path.isdir(target):
                console.print("[yellow]Directory detected → using 'dir'[/yellow]")
                return "dir", [target]
        return cmd, args
    
    def execute_external(self, cmd: str, args: List[str], full_line: str):
        """Execute external commands with error recovery"""
        try:
            if self.is_windows:
                # Windows needs shell=True for built-ins like 'dir'
                full_cmd = f"{cmd} {' '.join(args)}"
                subprocess.run(full_cmd, shell=True)
            else:
                subprocess.run([cmd] + args)
        except FileNotFoundError:
            # Smart Error Recovery!
            corrected = handle_command_not_found(cmd, full_line)
            
            if corrected:
                # Re-execute with corrected command
                console.print(f"[green]→ Running:[/green] {corrected}\n")
                execute_command(corrected)
            else:
                console.print(f"[red]Command not found:[/red] {cmd}")
        except Exception as e:
            console.print(f"[red]Execution error:[/red] {e}")

# Global executor instance
_executor = CommandExecutor()

def execute_command(command_line: str) -> bool:
    """
    Main execution function
    Returns: True to continue shell, False to exit
    """
    if not command_line.strip():
        return True
    
    # Parse command
    cmd, args = _executor.parse_command(command_line)
    if cmd is None:
        return True
    
    # Adapt command for OS compatibility
    cmd, args, proceed = adapt_command(cmd, args)
    if not proceed:
        return True
    
    # Smart type handler
    cmd, args = _executor.smart_type_handler(cmd, args)
    
    # Handle built-in commands (includes new features!)
    is_builtin, should_continue, new_path = _executor.handle_builtin(cmd, args)
    if is_builtin:
        # Handle project switcher path change
        if new_path:
            os.chdir(new_path)
        return should_continue
    
    # Execute external command (with error recovery)
    _executor.execute_external(cmd, args, command_line)
    return True