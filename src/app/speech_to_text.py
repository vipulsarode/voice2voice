from io import BytesIO
from groq import AsyncGroq

async def transcribe_audio_data(
        audio_data : bytes,
        api_client : AsyncGroq,
        model_name : str = 'whisper-large-v3-turbo',
        temperature : float = 0.0,
        language : str = 'en'
) -> str :
    with BytesIO(initial_bytes=audio_data) as audio_stream:
        audio_stream.name = 'audio.wav'
        response = await api_client.audio.transcriptions.create(
            model = model_name,
            file = audio_stream,
            temperature = temperature,
            language = language
        )

    text = response.text.strip()
    return text


