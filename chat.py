import os
import argparse
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

# Load environment variables
load_dotenv()
console = Console()

def main():
    # Setup CLI Arguments
    parser = argparse.ArgumentParser(description="Groq Stream Chat CLI")
    parser.add_argument("--model", default="llama-3.1-8b-instant", help="Groq model ID")
    parser.add_argument("--temp", type=float, default=0.7, help="Temperature (0.0-1.0)")
    parser.add_argument("--system", default="You are a helpful assistant.", help="System prompt")
    args = parser.parse_args()

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    current_model = args.model
    messages = [{"role": "system", "content": args.system}]
    
    # Session totals
    session_prompt_tokens = 0
    session_completion_tokens = 0

    console.print(Panel(
        f"Model: [bold cyan]{current_model}[/bold cyan]\nTemp: [bold yellow]{args.temp}[/bold yellow]", 
        title="Session Initialized", border_style="green"
    ))

    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()

            if user_input.lower() in ["exit", "quit"]:
                break

            messages.append({"role": "user", "content": user_input})

            full_response = ""
            console.print("[bold blue]Assistant:[/bold blue] ", end="")
            
            # REMOVED stream_options to ensure compatibility across all SDK versions
            stream = client.chat.completions.create(
                messages=messages,
                model=current_model,
                temperature=args.temp,
                stream=True,
            )

            for chunk in stream:
                # 1. Process Content
                if len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        print(content, end="", flush=True)
                
                # 2. Process Usage (Standard location for streaming)
                if hasattr(chunk, 'x_groq') and chunk.x_groq and chunk.x_groq.usage:
                    usage = chunk.x_groq.usage
                    p_tokens = usage.prompt_tokens
                    c_tokens = usage.completion_tokens
                    session_prompt_tokens += p_tokens
                    session_completion_tokens += c_tokens
                    
                    # Display usage table
                    print() 
                    table = Table(show_header=True, header_style="bold magenta", box=None)
                    table.add_column("Type")
                    table.add_column("Turn Tokens")
                    table.add_column("Total Session")
                    table.add_row("Prompt", str(p_tokens), str(session_prompt_tokens))
                    table.add_row("Completion", str(c_tokens), str(session_completion_tokens))
                    console.print(table)

            print() # Final newline
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

    console.print("[bold yellow]Goodbye![/bold yellow]")

if __name__ == "__main__":
    main()