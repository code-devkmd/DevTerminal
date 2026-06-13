"""
Quick HTTP Testing - Fast API testing from terminal
Beautiful output with syntax highlighting
"""
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Optional
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table

console = Console()


class HTTPTester:
    """Handles HTTP requests with pretty output"""
    
    def __init__(self):
        self.timeout = 10
        self.last_response = None
    
    def _format_url(self, url: str) -> str:
        """Add http:// if no scheme specified"""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url
    
    def _parse_headers(self, headers_dict) -> Dict[str, str]:
        """Parse headers into a clean dict"""
        result = {}
        for key, value in headers_dict.items():
            result[key] = value
        return result
    
    def _display_response(self, response, body: str, method: str, url: str):
        """Display response in a beautiful format"""
        # Status line
        status_color = "green" if 200 <= response.status < 300 else "red" if response.status >= 400 else "yellow"
        console.print(f"\n[{status_color}]{method} {url}[/{status_color}]")
        console.print(f"[{status_color}]Status: {response.status} {response.reason}[/{status_color}]\n")
        
        # Headers table
        headers = self._parse_headers(response.headers)
        
        if headers:
            table = Table(title="Response Headers", show_header=False, box=None)
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="dim")
            
            for key, value in headers.items():
                table.add_row(key, value)
            
            console.print(table)
            console.print()
        
        # Body
        if body:
            # Try to parse as JSON for pretty printing
            try:
                json_data = json.loads(body)
                json_str = json.dumps(json_data, indent=2)
                syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
                console.print(Panel(syntax, title="Response Body", border_style="blue"))
            except json.JSONDecodeError:
                # Not JSON, display as text
                console.print(Panel(body[:1000], title="Response Body", border_style="blue"))
                if len(body) > 1000:
                    console.print(f"[dim]... ({len(body)} bytes total)[/dim]")
    
    def get(self, url: str, headers: Dict[str, str] = None) -> bool:
        """Perform GET request"""
        url = self._format_url(url)
        
        try:
            req = urllib.request.Request(url, headers=headers or {})
            
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                body = response.read().decode('utf-8')
                self.last_response = (response, body)
                self._display_response(response, body, "GET", url)
                return True
                
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='ignore')
            self._display_response(e, body, "GET", url)
            return False
            
        except Exception as e:
            console.print(f"[red]Request failed:[/red] {e}")
            return False
    
    def post(self, url: str, data: str, headers: Dict[str, str] = None) -> bool:
        """Perform POST request"""
        url = self._format_url(url)
        
        # Parse data if it looks like JSON
        try:
            # Try to parse as JSON to validate
            json_data = json.loads(data)
            body_bytes = json.dumps(json_data).encode('utf-8')
            
            # Set content-type header
            if headers is None:
                headers = {}
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
                
        except json.JSONDecodeError:
            # Not JSON, send as-is
            body_bytes = data.encode('utf-8')
        
        try:
            req = urllib.request.Request(
                url,
                data=body_bytes,
                headers=headers or {},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                body = response.read().decode('utf-8')
                self.last_response = (response, body)
                self._display_response(response, body, "POST", url)
                return True
                
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='ignore')
            self._display_response(e, body, "POST", url)
            return False
            
        except Exception as e:
            console.print(f"[red]Request failed:[/red] {e}")
            return False
    
    def headers_only(self, url: str) -> bool:
        """Get only headers (HEAD request)"""
        url = self._format_url(url)
        
        try:
            req = urllib.request.Request(url, method='HEAD')
            
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                headers = self._parse_headers(response.headers)
                
                console.print(f"\n[green]HEAD {url}[/green]")
                console.print(f"[green]Status: {response.status}[/green]\n")
                
                table = Table(show_header=False, box=None)
                table.add_column("Key", style="cyan")
                table.add_column("Value", style="dim")
                
                for key, value in headers.items():
                    table.add_row(key, value)
                
                console.print(table)
                return True
                
        except Exception as e:
            console.print(f"[red]Request failed:[/red] {e}")
            return False


# Global instance
http_tester = HTTPTester()


def cmd_http(args: list) -> bool:
    """
    Handle 'http' command - GET request
    Usage: http <url>
    """
    if not args:
        console.print("[red]Usage:[/red] http <url>")
        return True
    
    url = args[0]
    http_tester.get(url)
    return True


def cmd_post(args: list) -> bool:
    """
    Handle 'post' command - POST request
    Usage: post <url> <json_data>
    """
    if len(args) < 2:
        console.print("[red]Usage:[/red] post <url> <json_data>")
        console.print("[dim]Example:[/dim] post localhost:3000/api/users '{\"name\":\"John\"}'")
        return True
    
    url = args[0]
    data = ' '.join(args[1:])  # Join remaining args as JSON data
    
    http_tester.post(url, data)
    return True


def cmd_headers(args: list) -> bool:
    """
    Handle 'headers' command - Get headers only
    Usage: headers <url>
    """
    if not args:
        console.print("[red]Usage:[/red] headers <url>")
        return True
    
    url = args[0]
    http_tester.headers_only(url)
    return True