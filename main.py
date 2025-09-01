from dotenv import load_dotenv
import os

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from api import get_weather_city

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=(
            "You are a helpful and knowledgeable voice AI assistant specializing in providing current weather information. "
            "You speak clearly and naturally. Ask for the location if the user hasn't mentioned it. "
            "Use the weather tool to fetch real-time weather for any city. "
            "When providing weather, be concise and directly answer the user's query."
        ))

    @function_tool()
    async def get_current_weather(self, location: str) -> str:
        """
        Returns current weather for the given location, like 'New York' or 'Istanbul'.
        This tool calls an external API to get real-time weather data.
        """
        return get_weather_city(location)


async def entrypoint(ctx: agents.JobContext):
    assistant = Assistant()

    llm = openai.LLM(
        model="gpt-4o-mini",
    )

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=llm,
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await ctx.connect()

    await session.generate_reply(instructions="Greet the user and offer weather assistance.")


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
