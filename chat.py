import os
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown


load_dotenv()


console = Console()

def main():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    MODEL = "llama-3.1-8b-instant"

    console.print(Panel(f"Connected to [bold cyan]{MODEL}[/bold cyan]", title="System", border_style="green"))

    user_input = "Write a short poem about love."
    console.print(f"\n[bold green]You:[/bold green] {user_input}")

    
    full_response = ""
    
    console.print("[bold blue]Assistant:[/bold blue] ", end="")
    
    try:
       
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model=MODEL,
            stream=True,
        )

       
        for chunk in stream:
            
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                
                print(delta, end="", flush=True)

        print("\n") 
        
        
        console.print(Panel(Markdown(full_response), title="Final Response", border_style="blue"))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()