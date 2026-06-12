import os
import sys
from colorama import Fore, Style, init
from devcli.core.shell import run_shell

# Initialize colorama once
init(autoreset=True)

def show_intro():
    banner = f"""{Fore.GREEN}
    ██████╗ ███████╗██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
    ██╔══██╗██╔════╝██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
    ██║  ██║█████╗  ██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
    ██║  ██║██╔══╝  ╚██╗ ██╔╝   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
    ██████╔╝███████╗ ╚████╔╝    ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
    ╚═════╝ ╚══════╝  ╚═══╝     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
{Style.RESET_ALL}"""
    
    info = f"""{Fore.CYAN}➤ DevTerminal
{Fore.YELLOW}➤ Version   : 2.0.0
➤ Engine    : DevCLI Core
➤ Mode      : Interactive Shell + AutoComplete
➤ Platform  : Cross-Platform{Style.RESET_ALL}
{Fore.MAGENTA}{'─' * 60}{Style.RESET_ALL}
"""
    
    print(banner + info)

def main():
    """Main entry point"""
    try:
        # Clear screen 
        os.system('cls' if os.name == 'nt' else 'clear')
        show_intro()
        run_shell()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()