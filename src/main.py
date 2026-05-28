import time
import click
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.brain import get_fast_llm
from src.agents.router import classify_intent, handle_intent

console = Console()

@click.command()
def cli():
    """Sexta-Feira V2 - Assistente de Terminal."""
    
    # Inicializa o modelo rápido
    try:
        fast_llm = get_fast_llm()
    except Exception as e:
        console.print(f"[bold red]Erro ao conectar com o Cérebro:[/bold red] {e}")
        return

    console.print(Panel.fit(
        "[bold cyan]Sexta-Feira V2[/bold cyan] online.\nSistemas nominais. Digite [bold yellow]'sair'[/bold yellow] para encerrar.", 
        border_style="cyan"
    ))
    
    # Injeta a personalidade e a regra de idiomas
    system_prompt = SystemMessage(content=(
        "Você é a Sexta-Feira (Friday), uma assistente de inteligência artificial avançada. "
        "Suas linguagens principais são Português (primário) e Inglês (secundário). "
        "Seja direta, formal, elegante e ocasionalmente sarcástica (no estilo Jarvis). "
        "Formate sempre suas respostas usando Markdown."
    ))
    chat_history = [system_prompt]
    
    while True:
        try:
            user_input = console.input("\n[bold green]Samuel:[/bold green] ")
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                console.print("[bold cyan]Sexta-Feira:[/bold cyan] Desligando sistemas. Até logo, senhor.")
                break
            if not user_input.strip():
                continue

            chat_history.append(HumanMessage(content=user_input))
            
            # Janela Deslizante: Mantém a SystemMessage (índice 0) + últimas 10 mensagens
            if len(chat_history) > 11:
                chat_history = [chat_history[0]] + chat_history[-10:]

            # Step 1: Classify intent with visual feedback
            with console.status("[bold yellow]🤔 Analisando intenção...[/bold yellow]", spinner="dots"):
                intent = classify_intent(user_input)

            # Step 2: Route to appropriate handler
            console.print("[bold cyan]Sexta-Feira:[/bold cyan]", end="\n")
            
            start_time = time.time()
            full_response = ""
            
            handler_type, handler_response = handle_intent(intent, user_input)
            
            # Step 3: Execute appropriate response
            if handler_type == "chat":
                # Standard chat flow - use Fast Model with streaming
                with Live(Markdown(""), console=console, refresh_per_second=60, transient=False) as live:
                    for chunk in fast_llm.stream(chat_history):
                        full_response += chunk.content
                        live.update(Markdown(full_response))
            
            elif handler_type in ["rag", "tool", "curation"]:
                # Tool calling - use handler response directly
                full_response = handler_response
                # Display with Rich formatting
                console.print(Markdown(full_response))
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            # Aproximação simples de tokens (1 token ≈ 4 caracteres no Llama)
            tokens = len(full_response) // 4 
            tps = tokens / elapsed if elapsed > 0 else 0
            
            console.print(f"[dim italic]> *⏱️ {elapsed:.2f}s | 🪙 ~{tokens} tokens | ⚡ {tps:.1f} t/s*[/dim italic]")
            
            chat_history.append(AIMessage(content=full_response))
            
        except KeyboardInterrupt:
            console.print("\n[bold cyan]Sexta-Feira:[/bold cyan] Cancelado. Digite 'sair' para finalizar o processo.")

if __name__ == '__main__':
    cli()