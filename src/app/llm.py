from dataclasses import dataclass
from typing import Literal

import aiohttp
from groq import AsyncGroq
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.groq import GroqModel

from app.settings import Settings

AvailableCities = Literal["Paris", "New York", "London"]

@dataclass
class Dependencies:
    settings : Settings
    session : aiohttp.ClientSession

async def get_weather(ctx : RunContext[Dependencies], cities : AvailableCities) -> str:
    url = "http://api.weatherstack.com/current"
    params = {
        'access_key' : ctx.deps.settings.weatherstack_api,
        'query' : cities
    }

    async with ctx.deps.session.get(url=url, params=params) as response:
        data = await response.json()
        observation_time = data.get('current').get('observation_time')
        temperature = data.get('current').get('temperature')
        weather_description = data.get('current').get('weather_descriptions')
        return f"At {observation_time}, the temperature in {cities} is {temperature}°C. The weather is {weather_description[0].lower()}"
    
#getting the model

def create_groq_model(groq_client : AsyncGroq) -> GroqModel:
    return GroqModel(model_name="llama-3.3-70b-versatile", groq_client=groq_client)

#creating Agent

def create_groq_agent(groq_model : GroqModel, tools: list[Tool[Dependencies]], system_prompt : str) -> Agent:
    return Agent(model = groq_model, deps_type = Dependencies, tools = tools, system_prompt = system_prompt)
    

