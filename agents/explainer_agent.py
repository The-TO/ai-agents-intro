"""Explainer Agent: explains a programming topic for beginners."""
from google.adk.agents import Agent

from agents.agent_runner import get_model, run_agent

EXPLAINER_INSTRUCTION = """You are an explainer agent for beginner programmers.
You receive a programming topic. Explain it simply and accurately.

Answer ONLY in Markdown, with exactly these three sections, in this order:

## Simple Explanation
Two or three short paragraphs. No jargon without a definition.

## Key Concepts
A bullet list of 3 to 5 concepts. Format: - **Concept**: one sentence.

## Example
One short code example in a fenced code block, then one sentence
explaining what it does.

Rules:
- Do not add other sections.
- Do not invent libraries or functions that do not exist.
- Keep the whole answer under 350 words.
"""

def create_explainer_agent():
    """Creer l'agent qui explique"""
    return Agent(
        name="explainer_agent",                         # identifiant, sans espace
        model=get_model(),                                # le modèle via LiteLLM
        description="Explains a programming topic.",    # à quoi il sert (1 phrase)
        instruction=EXPLAINER_INSTRUCTION,              # LE comportement
    )


async def run_explainer_agent(topic):
    """Run the Explainer Agent on a topic and return its Markdown."""
    agent = create_explainer_agent()
    return await run_agent(agent, f"Topic: {topic}")