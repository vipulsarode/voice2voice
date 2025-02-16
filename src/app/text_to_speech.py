from types import TracebackType
from typing import AsyncIterator, Literal

from openai import AsyncOpenAI

Voice = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
ResponseFormat = Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]


class TextToSpeech:

    def __init__(self, client : AsyncOpenAI, model_name : str, voice : Voice = 'echo', 
                 response_format : ResponseFormat = 'aac', speed : float = 1, buffer_size : int = 64, sentence_endings: tuple[str, ...] = (
            ".",
            "?",
            "!",
            ";",
            ":",
            "\n",
        ), chunk_size : int = 1024 * 5) -> None:
        self.client = client
        self.model_name = model_name
        self.voice: Voice = voice
        self.response_format: ResponseFormat = response_format
        self.speed = speed
        self.buffer_size = buffer_size
        self.sentence_endings = sentence_endings
        self.chunk_size = chunk_size
        self._buffer = ""

    async def __aenter__(self):
        '''
        Enters the asynchronous context manager
        Returns: TextToSpeech
        '''
        return self
    
    async def feed(self, text : str) -> AsyncIterator[bytes]:
        '''
        Feed the text into buffer until the max buffer size is reached or sentence ends and yields audio bytes.

        Args: Text

        Returns: Audio Bytes
        '''

        self._buffer += text

        if len(self._buffer) > self.buffer_size or any(self._buffer.endswith(i) for i in self.sentence_endings):

            async for chunk in self.flush():
                yield chunk

    async def flush(self) -> AsyncIterator[bytes]:
        '''
        Flushes the buffered text and yields audio bytes

        Yields: Audio Bytes 
        '''

        if self._buffer:
            async for chunk in self._send_audio(self._buffer):
                yield chunk
            self._buffer = ''

    async def _send_audio(self, text: str) -> AsyncIterator[bytes]:
            async with self.client.audio.speech.with_streaming_response.create(
            model=self.model_name,
            input=text,
            voice=self.voice,
            response_format=self.response_format,
            speed=self.speed,
        ) as audio_stream:
                async for audio_chunk in audio_stream.iter_bytes(
                    chunk_size=self.chunk_size
                ):
                    yield audio_chunk

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exits the asynchronous context manager.
        """
        pass