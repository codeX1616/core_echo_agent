# Core Echo

## About the Project
Core Echo is an advanced voice-driven AI agent orchestration system. It acts as a central hub that listens to user commands via voice, processes the audio, and dynamically routes or creates agents to handle the requested tasks. It features a Human-In-The-Loop (HITL) safety mechanism for destructive actions and a sandbox environment for executing plugins securely.

## Use Case
This project is designed for developers or power users who want a hands-free, voice-activated AI assistant capable of performing a wide range of tasks locally. It can dynamically generate new agents on the fly if it doesn't have a pre-existing one for a specific request. The built-in web dashboard provides real-time visibility into the system's state, listening status, and agent execution.

## Project Setup
1. Clone the repository and navigate into the project directory.
2. It is highly recommended to create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This project relies on local models and ML libraries such as `torch`, `whisper-cpp-python`, `llama-cpp-python`, and `qdrant-client`.)*

## Running the Application
To start the Core Echo assistant and the dashboard server:
```bash
python main.py
```
This will start listening to your voice input and simultaneously launch a local web dashboard (typically accessible at `http://127.0.0.1:8000`).
