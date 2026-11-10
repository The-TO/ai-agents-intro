"""Shared code for every agent: build the model and run an agent."""
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from config import get_model_name

APP_NAME = "study_guide_generator"
USER_ID = "student"


def get_model():
    """Build the LiteLLM connector from the MODEL_NAME variable."""
    return LiteLlm(model=get_model_name())


async def run_agent(agent, prompt):
    """Send one message to an agent and return its final text answer."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            parts = event.content.parts or []
            final_text = "".join(part.text or "" for part in parts)

    if not final_text.strip():
        raise RuntimeError(f"{agent.name} returned an empty answer.")
    return final_text.strip()