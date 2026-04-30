import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

def main():
    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


    MODEL = "llama-3.1-8b-instant"

    print(f"--- Sending request to {MODEL} ---")

    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain what an LLM is in one sentence.",
            }
        ],
        model=MODEL,
    )

    
    content = chat_completion.choices[0].message.content
    print(f"Assistant: {content}")

if __name__ == "__main__":
    main()