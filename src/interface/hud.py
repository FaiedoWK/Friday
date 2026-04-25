from rich.layout import Layout
from rich.panel import Panel

def get_base_layout():
    """
    Cores: Azul-claro (sky_blue2), Cinza (grey84) e Ciano.
    """
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body")
    )
    
    # Header minimalista
    layout["header"].update(
        Panel(
            "[bold sky_blue2]Sexta-Feira V2[/bold sky_blue2] [grey84]// LLM Local Agent[/grey84]", 
            border_style="cyan"
        )
    )
    
    return layout

def get_status_panel(status: str, intent: str = "N/A"):
    """Retorna um painel lateral de status para manter o visual limpo."""
    return Panel(
        f"[grey84]Status:[/grey84] [sky_blue2]{status}[/sky_blue2]\n[grey84]Intent:[/grey84] [cyan]{intent}[/cyan]",
        title="[bold sky_blue2]System Monitor[/bold sky_blue2]",
        border_style="sky_blue2",
        width=30
    )