"""
Quick Project Switcher - Jump between projects instantly
Remembers recent projects and auto-detects environment
"""
import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

# Project database location
PROJECTS_FILE = Path.home() / ".devterminal" / "projects.json"
PROJECTS_FILE.parent.mkdir(exist_ok=True)


class Project:
    """Represents a saved project"""
    def __init__(self, name: str, path: str, last_accessed: str = None):
        self.name = name
        self.path = path
        self.last_accessed = last_accessed or datetime.now().isoformat()
        self.type = self._detect_type()
    
    def _detect_type(self) -> str:
        """Detect project type based on files"""
        path = Path(self.path)
        
        if not path.exists():
            return "unknown"
        
        # Check for various project markers
        if (path / "package.json").exists():
            return "node"
        elif (path / "requirements.txt").exists() or (path / "setup.py").exists():
            return "python"
        elif (path / "Cargo.toml").exists():
            return "rust"
        elif (path / "go.mod").exists():
            return "go"
        elif (path / "pom.xml").exists() or (path / "build.gradle").exists():
            return "java"
        elif (path / "Gemfile").exists():
            return "ruby"
        elif (path / "composer.json").exists():
            return "php"
        elif (path / ".git").exists():
            return "git"
        else:
            return "folder"
    
    def get_info(self) -> Dict[str, str]:
        """Get detailed project information"""
        info = {
            "type": self.type,
            "git_branch": self._get_git_branch(),
            "venv": self._has_venv()
        }
        return info
    
    def _get_git_branch(self) -> Optional[str]:
        """Get current git branch if it's a git repo"""
        try:
            result = subprocess.run(
                ['git', '-C', self.path, 'branch', '--show-current'],
                capture_output=True,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _has_venv(self) -> bool:
        """Check if project has virtual environment"""
        venv_dirs = ['venv', '.venv', 'env', '.env']
        path = Path(self.path)
        
        for venv in venv_dirs:
            if (path / venv).exists():
                return True
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        return {
            "name": self.name,
            "path": self.path,
            "last_accessed": self.last_accessed
        }


class ProjectManager:
    """Manages project switching and tracking"""
    
    def __init__(self):
        self.projects = self._load_projects()
    
    def _load_projects(self) -> List[Project]:
        """Load projects from JSON file"""
        if not PROJECTS_FILE.exists():
            return []
        
        try:
            with open(PROJECTS_FILE, 'r') as f:
                data = json.load(f)
                return [Project(**p) for p in data]
        except Exception as e:
            console.print(f"[red]Error loading projects:[/red] {e}")
            return []
    
    def _save_projects(self):
        """Save projects to JSON file"""
        try:
            data = [p.to_dict() for p in self.projects]
            with open(PROJECTS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving projects:[/red] {e}")
    
    def add_project(self, name: str, path: str) -> bool:
        """Add or update a project"""
        # Check if path exists
        if not Path(path).exists():
            console.print(f"[red]Path does not exist:[/red] {path}")
            return False
        
        # Check if project with this name exists
        existing = self.get_project(name)
        if existing:
            # Update existing
            existing.path = path
            existing.last_accessed = datetime.now().isoformat()
        else:
            # Add new
            project = Project(name, path)
            self.projects.append(project)
        
        self._save_projects()
        console.print(f"[green]✓ Project '{name}' saved[/green]")
        return True
    
    def get_project(self, name: str) -> Optional[Project]:
        """Get project by name"""
        for p in self.projects:
            if p.name.lower() == name.lower():
                return p
        return None
    
    def remove_project(self, name: str) -> bool:
        """Remove a project"""
        project = self.get_project(name)
        if project:
            self.projects.remove(project)
            self._save_projects()
            console.print(f"[green]✓ Project '{name}' removed[/green]")
            return True
        else:
            console.print(f"[yellow]Project '{name}' not found[/yellow]")
            return False
    
    def list_projects(self):
        """Display all projects in a table"""
        if not self.projects:
            console.print("[yellow]No projects saved yet[/yellow]")
            console.print("\n[dim]Add a project with:[/dim] proj add <name> <path>")
            return
        
        # Sort by last accessed (most recent first)
        sorted_projects = sorted(
            self.projects,
            key=lambda p: p.last_accessed,
            reverse=True
        )
        
        table = Table(title="Saved Projects", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Path", style="blue")
        table.add_column("Git", style="cyan")
        
        for p in sorted_projects:
            info = p.get_info()
            git_info = info['git_branch'] or "-"
            
            table.add_row(
                p.name,
                p.type,
                p.path,
                git_info
            )
        
        console.print(table)
    
    def switch_to(self, name: str) -> Optional[str]:
        """
        Switch to a project
        Returns: path to switch to, or None if failed
        """
        project = self.get_project(name)
        
        if not project:
            console.print(f"[red]Project '{name}' not found[/red]")
            console.print("\n[dim]Available projects:[/dim]")
            self.list_projects()
            return None
        
        # Update last accessed
        project.last_accessed = datetime.now().isoformat()
        self._save_projects()
        
        # Get project info
        info = project.get_info()
        
        # Display info
        console.print(f"\n[green]→ Switching to:[/green] {project.name}")
        console.print(f"[dim]Path:[/dim] {project.path}")
        console.print(f"[dim]Type:[/dim] {info['type']}")
        
        if info['git_branch']:
            console.print(f"[dim]Branch:[/dim] {info['git_branch']}")
        
        if info['venv']:
            console.print("[yellow]💡 Virtual environment detected[/yellow]")
        
        return project.path


# Global instance
project_manager = ProjectManager()


def cmd_proj(args: List[str]) -> tuple:
    """
    Handle 'proj' command
    Usage:
      proj list                  - List all projects
      proj add <name> [path]     - Add current/specified directory
      proj remove <name>         - Remove a project
      proj <name>                - Switch to project
    
    Returns: (continue, new_path_to_cd)
    """
    if not args:
        project_manager.list_projects()
        return True, None
    
    subcommand = args[0].lower()
    
    if subcommand == "list":
        project_manager.list_projects()
        return True, None
    
    elif subcommand == "add":
        if len(args) < 2:
            console.print("[red]Usage:[/red] proj add <name> [path]")
            return True, None
        
        name = args[1]
        path = args[2] if len(args) > 2 else os.getcwd()
        path = os.path.abspath(path)
        
        project_manager.add_project(name, path)
        return True, None
    
    elif subcommand == "remove":
        if len(args) < 2:
            console.print("[red]Usage:[/red] proj remove <name>")
            return True, None
        
        name = args[1]
        project_manager.remove_project(name)
        return True, None
    
    else:
        # Treat as project name to switch to
        name = subcommand
        path = project_manager.switch_to(name)
        
        if path:
            return True, path
        return True, None