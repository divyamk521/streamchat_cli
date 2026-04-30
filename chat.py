import os
import argparse
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table


load_dotenv()
console = Console()

def main():
    
    parser = argparse.ArgumentParser(description="Groq Stream Chat CLI")
    parser.add_argument("--model", default="llama-3.1-8b-instant", help="Groq model ID")
    parser.add_argument("--temp", type=float, default=0.7, help="Temperature (0.0-1.0)")
    parser.add_argument("--system", default="You are a helpful, concise assistant.", help="System prompt")
    args = parser.parse_args()

    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    current_model = args.model
    messages = [{"role": "system", "content": args.system}]
    
    console.print(Panel(
        f"Model: [bold cyan]{current_model}[/bold cyan]\nTemp: [bold yellow]{args.temp}[/bold yellow]\nSystem: [italic]{args.system}[/italic]", 
        title="Session Initialized", border_style="green"
    ))

    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                break

            
            if user_input.startswith("/model "):
                new_model = user_input.split(" ")[1]
                current_model = new_model
                console.print(f"[bold yellow]Model switched to {current_model}[/bold yellow]")
                continue

            messages.append({"role": "user", "content": user_input})

            full_response = ""
            console.print("[bold blue]Assistant:[/bold blue] ", end="")
            
            
            stream = client.chat.completions.create(
                messages=messages,
                model=current_model,
                temperature=args.temp,
                stream=True,
            )

            for chunk in stream:
                
                if len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        print(content, end="", flush=True)

            print() 
            messages.append({"role": "assistant", "content": full_response})

            
            console.print("[dim]------------------------------------[/dim]")

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Session ended.[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    console.print("[bold yellow]Goodbye![/bold yellow]")

if __name__ == "__main__":
    main()