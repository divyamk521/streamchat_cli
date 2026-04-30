# Day 1: LLM Streaming Chat CLI

A high-performance, terminal-based chatbot built with Python and Groq. This project demonstrates the core foundations of AI engineering: streaming, conversation memory, and token management.

## 🚀 Features
- **Ultra-fast Streaming**: Real-time token output using Groq's Llama-3.1 models.
- **Persistent Memory**: Maintains conversation context across multiple turns.
- **Live Token Tracking**: Real-time monitoring of prompt and completion tokens per turn and per session.
- **Rich Terminal UI**: Beautifully formatted output with panels, markdown support, and status tables.
- **CLI Customization**: Switch models and adjust temperature settings via command-line arguments.

## 🛠️ Tech Stack
- **Language**: Python 3.11+
- **Inference**: Groq SDK (Llama-3.1-8b-instant)
- **UI/Formatting**: Rich
- **Environment**: python-dotenv

## 📋 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd day01-chat-cli

2.**Set up virtual environment:**

Bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

3. **Configure Environment:**
Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key_here

3. **Run the App:**
python chat.py --model llama-3.1-8b-instant --temp 0.7

