from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

import aiohttp
from fastapi import FastAPI
from groq import AsyncGroq
from loguru import logger
from openai import AsyncOpenAI
from pydantic_ai import Agent, Tool
from pydantic_ai.models.groq import GroqModel

from app.llm import Dependencies, create_groq_agent, get_weather
from app.settings import Settings, get_settings

def create_aiohttp_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession()

def create_groq_client(
    settings: Settings,
) -> AsyncGroq:
    return AsyncGroq(api_key=settings.groq_api)


def create_openai_client(
    settings: Settings,
) -> AsyncOpenAI:
    return AsyncOpenAI(api_key=settings.openai_api_key)


def create_groq_model(
    groq_client: AsyncGroq,
) -> GroqModel:
    return GroqModel(
        model_name="llama-3.3-70b-versatile",
        groq_client=groq_client,
    )

class State(TypedDict):
    aiohttp_session: aiohttp.ClientSession
    groq_client: AsyncGroq
    openai_client: AsyncOpenAI
    groq_agent: Agent[Dependencies]

@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[State]:
    settings = get_settings()
    aiohttp_session = create_aiohttp_session()
    openai_client = create_openai_client(settings=settings)
    groq_client = create_groq_client(settings=settings)
    _groq_model = create_groq_model(groq_client=groq_client)

    groq_agent = create_groq_agent(
        groq_model=_groq_model,
        tools = [Tool(function=get_weather, takes_ctx=True)],
        system_prompt = ("You are a helpful assistant. "
            "You interact with the user in a natural way. "
            "You should use `get_weather` ONLY to provide weather information."
    )
)

    yield {
        "aiohttp_session" : aiohttp_session,
        'groq_agent' : groq_agent,
        "openai_client" : openai_client,
        'groq_client' : groq_client 
    }

    logger.info("Closing aiohttp session")
    await aiohttp_session.close()

    logger.info("Closing OpenAI client")
    await openai_client.close()

    logger.info("Closing Groq client")
    await groq_client.close()