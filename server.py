from fastapi import Depends, FastAPI, WebSocket
from groq import AsyncGroq
from pydantic_ai import Agent
from pathlib import Path
from fastapi.responses import HTMLResponse

from src.app.lifespan import app_lifespan as lifespan
from src.app.llm import Dependencies
from src.app.settings import get_settings
from src.app.speech_to_text import transcribe_audio_data
from src.app.text_to_speech import TextToSpeech

app = FastAPI(title = 'Voice to Voice Demo', lifespan = lifespan)

@app.get("/")
async def get():
    with Path("sample_ui.html").open("r") as file:
        return HTMLResponse(file.read()) # This will render the HTML

async def get_agent_dependencies(websocket: WebSocket) -> Dependencies:
    return Dependencies(
        settings=get_settings(),
        session=websocket.state.aiohttp_session,
    )


async def get_groq_client(websocket: WebSocket) -> AsyncGroq:
    return websocket.state.groq_client


async def get_agent(websocket: WebSocket) -> Agent:
    return websocket.state.groq_agent


async def get_tts_handler(websocket: WebSocket) -> TextToSpeech:
    return TextToSpeech(
        client=websocket.state.openai_client,
        model_name="tts-1",
        response_format="aac",
    )

@app.websocket('/voice_stream')
async def voice_to_voice(
    websocket: WebSocket,
    groq_client : AsyncGroq = Depends(get_groq_client),
    agent: Agent[Dependencies] = Depends(get_agent),
    agent_deps : Dependencies = Depends(get_agent_dependencies),
    tts_handler : TextToSpeech = Depends(get_tts_handler)
):
    '''WebSocket endpoint for voice-to-voice communication.

    - Receives audio bytes from the client
    - Transcribes the audio to text
    - generates a response using the language model agent
    - converts the response text to speech, and streams the audio bytes back to the client.

    Args:
        websocket: WebSocket connection.
        conversation_id: Unique identifier for the conversation (dependency).
        db_conn: Asynchronous database connection (dependency).
        groq_client: Groq API client for transcription (dependency).
        agent: Language model agent for generating responses (dependency).
        agent_deps: Dependencies for the agent (dependency).
        tts_handler: Text-to-Speech handler for converting text to audio (dependency)'''
    
    await websocket.accept()

    async for incoming_audio_bytes in websocket.iter_bytes():
        transcription = await transcribe_audio_data(
            audio_data = incoming_audio_bytes,
            api_client = groq_client
        )

        generation = ''

        async with tts_handler:
            async with agent.run_stream(
                user_prompt = transcription,
                deps = agent_deps
            ) as result:
                async for message in result.stream_text(delta = True):
                    generation += message

                    async for audio_chunk in tts_handler.feed(text = message):
                        await websocket.send_bytes(data=audio_chunk)

            async for audio_chunk in tts_handler.flush():
                await websocket.send_bytes(data=audio_chunk)
