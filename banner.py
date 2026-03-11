# Initialize colorama for cross-platform color support
import pyfiglet
from colorama import init, Fore, Style
from rich.console import Console
from rich.panel import Panel

console = Console()
init(autoreset=True)

def print_banner():
    # Generate the ASCII art
    # Common fonts: 'slant', 'banner3-D', 'block', 'bubble'
    banner_text = pyfiglet.figlet_format("CLAUDE CODE CLONE", font="small")
    
    #print(f"{Fore.CYAN}{Style.BRIGHT}{banner_text}")
    console.print(Panel(banner_text, subtitle="The Unofficial Claude Clone", border_style="magenta"), style="bold color(27)")
    print(f"{Fore.YELLOW}v1.0.0 | Built with Python & Love\n")

if __name__ == "__main__":
    print_banner()