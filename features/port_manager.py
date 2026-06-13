"""
Port Manager - Shows and manages running processes on ports
Cross-platform port monitoring and management
"""
import os
import re
import subprocess
import psutil
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

console = Console()


class PortInfo:
    """Information about a process using a port"""
    def __init__(self, port: int, pid: int, name: str, status: str = ""):
        self.port = port
        self.pid = pid
        self.name = name
        self.status = status


class PortManager:
    """Cross-platform port manager"""
    
    def __init__(self):
        self.is_windows = os.name == 'nt'
    
    def get_all_ports(self) -> List[PortInfo]:
        """Get all processes listening on ports"""
        ports = []
        
        try:
            # Use psutil for cross-platform compatibility
            connections = psutil.net_connections(kind='inet')
            
            for conn in connections:
                if conn.status == 'LISTEN' and conn.laddr:
                    port = conn.laddr.port
                    pid = conn.pid
                    
                    if pid:
                        try:
                            process = psutil.Process(pid)
                            name = process.name()
                            status = conn.status
                            
                            ports.append(PortInfo(port, pid, name, status))
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
        
        except Exception as e:
            console.print(f"[red]Error getting ports:[/red] {e}")
        
        return ports
    
    def get_port_info(self, port: int) -> Optional[PortInfo]:
        """Get information about a specific port"""
        all_ports = self.get_all_ports()
        
        for port_info in all_ports:
            if port_info.port == port:
                return port_info
        
        return None
    
    def kill_process_on_port(self, port: int) -> bool:
        """Kill process running on specified port"""
        port_info = self.get_port_info(port)
        
        if not port_info:
            console.print(f"[yellow]No process found on port {port}[/yellow]")
            return False
        
        console.print(
            f"[yellow]Found:[/yellow] {port_info.name} "
            f"[dim](PID: {port_info.pid})[/dim] on port {port}"
        )
        
        if not Confirm.ask(f"Kill this process?", default=False):
            console.print("[dim]Cancelled[/dim]")
            return False
        
        try:
            process = psutil.Process(port_info.pid)
            process.terminate()
            
            # Wait a bit and force kill if still alive
            try:
                process.wait(timeout=3)
            except psutil.TimeoutExpired:
                process.kill()
            
            console.print(f"[green]✓ Killed process on port {port}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Failed to kill process:[/red] {e}")
            return False
    
    def find_by_name(self, name: str) -> List[PortInfo]:
        """Find all ports used by processes matching name"""
        all_ports = self.get_all_ports()
        matches = []
        
        name_lower = name.lower()
        for port_info in all_ports:
            if name_lower in port_info.name.lower():
                matches.append(port_info)
        
        return matches
    
    def display_ports(self, ports: List[PortInfo] = None):
        """Display ports in a nice table"""
        if ports is None:
            ports = self.get_all_ports()
        
        if not ports:
            console.print("[yellow]No active ports found[/yellow]")
            return
        
        # Sort by port number
        ports.sort(key=lambda x: x.port)
        
        # Create table
        table = Table(title="Active Ports", show_header=True, header_style="bold cyan")
        table.add_column("Port", style="green", width=8)
        table.add_column("PID", style="blue", width=8)
        table.add_column("Process", style="yellow")
        table.add_column("Status", style="dim")
        
        for port in ports:
            table.add_row(
                str(port.port),
                str(port.pid),
                port.name,
                port.status
            )
        
        console.print(table)


# Global instance
port_manager = PortManager()


def cmd_ports(args: List[str]) -> bool:
    """
    Handle 'ports' command
    Usage:
      ports           - Show all ports
      ports <name>    - Show ports for specific process
    """
    if args:
        # Search by process name
        name = args[0]
        matches = port_manager.find_by_name(name)
        
        if matches:
            port_manager.display_ports(matches)
        else:
            console.print(f"[yellow]No processes found matching '{name}'[/yellow]")
    else:
        # Show all ports
        port_manager.display_ports()
    
    return True


def cmd_kill_port(args: List[str]) -> bool:
    """
    Handle 'kill-port' command
    Usage: kill-port <port_number>
    """
    if not args:
        console.print("[red]Usage:[/red] kill-port <port_number>")
        return True
    
    try:
        port = int(args[0])
        port_manager.kill_process_on_port(port)
    except ValueError:
        console.print(f"[red]Invalid port number:[/red] {args[0]}")
    
    return True