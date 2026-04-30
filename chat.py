import os
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


load_dotenv()


console = Console()

def main():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    MODEL = "llama-3.1-8b-instant"

   
    messages = [
        {
            "role": "system",
            "content": "You are a helpful, witty, and concise AI assistant. Use markdown for formatting."
        }
    ]

    console.print(Panel(f"Connected to [bold cyan]{MODEL}[/bold cyan]\nMemory: [italic]Active[/italic]", 
                        title="System", border_style="green"))

    
    while True:
        try:
           
            user_input = console.input("\n[bold green]You:[/bold green] ")

            
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("[bold yellow]Goodbye![/bold yellow]")
                break

            
            messages.append({"role": "user", "content": user_input})

            console.print("[bold blue]Assistant:[/bold blue] ", end="")
            
            full_response = ""
            
            
            stream = client.chat.completions.create(
                messages=messages,
                model=MODEL,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    print(delta, end="", flush=True)

            print() 
            
            
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Session ended by user.[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            break

if __name__ == "__main__":
    main()