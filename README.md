
# Voice-to-Voice Chatbot

This project is a voice-to-voice chatbot that leverages the Groq API, OpenAI API, and Pydantic AI Agents to create a seamless conversational experience. The chatbot listens to user input via voice, processes the input using advanced AI models, and responds with synthesized voice output. This repository contains the code, setup instructions, and documentation to help you get started with the project.

## Features

Voice Input: The chatbot accepts voice input from the user, converting speech to text using Whisper speech-to-text model from Groq API.

AI-Powered Responses: Utilizes the powerful llama-7b model for natural language understanding and generation, ensuring high-quality conversational responses.

Pydantic AI Agents: These Agents understand your query and give you real time weather details of cities acrros the globe.

Voice Output: Converts the chatbot's text responses back into natural-sounding speech using text-to-speech (TTS) model from OpenAI.

## Prerequisites
Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- Pydantic
- FastAPI
- UV (for dependency management)
- API keys for:
    - OpenAI API
    - Groq API



## Installation
#### Clone the repository:

```bash
https://github.com/vipulsarode/voice2voice.git
cd voice2voice
```

#### Install dependencies using UV:

```bash
uv pip install .
```

#### Set up your environment variables:

Create a .env file in the root directory and add your API keys:

```python
OPENAI_API=your_openai_api_key
GROQ_API=your_groq_api_key
WEATHERSTACK_API=your_weatherstack_api_key
```

#### Run the chatbot:

```bash
uv run uvicorn server:app \                                        
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

## Structure
```
voice2voice/
├── __pycache__/                   
├── src/                            
│   ├── app/                        
│   │   └── __pycache__/            
│   ├── __init__.py                 
│   ├── lifespan.py                 # Contains lifecycle management code (e.g., startup/shutdown logic)
│   ├── llm.py                      # Contains code related to language models (LLM)
│   ├── settings.py                 # Configuration settings for the project
│   ├── speech_to_text.py           # Handles speech-to-text conversion functionality
│   └── text_to_speech.py           # Handles text-to-speech conversion functionality
├── .gitignore                      
├── .python-version                 
├── pyproject.toml                  
├── README.md                       
├── sample_ui.html                  # Sample HTML file for the user interface
└── server.py                       # Main server script for running the application
```

## Future Work
This project is a work in progress, and there are several areas for improvement and expansion:

Multi-Language Support: Add support for multiple languages in both voice input and output.

Customizable Voice: Allow users to choose from different voices or customize the chatbot's voice characteristics.

Conversation History: Implement a persistent conversation history to enable context-aware interactions across sessions i.e integrating database.

Integration with Other APIs: Expand functionality by integrating with additional APIs (e.g., weather, news, or calendar services).

Deployment: Package the chatbot as a deployable application (e.g., Docker container) for easier distribution and scaling.

User Interface: Develop a web or mobile interface for a more user-friendly experience.




## License
[MIT](https://choosealicense.com/licenses/mit/)
##
Feel free to reach out if you have any questions or suggestions! Happy coding! 🚀

