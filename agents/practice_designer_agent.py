"""Practice Designer Agent: creates a small exercise from an explanation."""
from google.adk.agents import Agent

from agents.agent_runner import get_model, run_agent

PRACTICE_INSTRUCTION = """You are a practice designer agent.
You receive a programming topic and an explanation written by another agent.
Create ONE short beginner-friendly exercise based on that explanation.
The exercise must take 10 to 20 minutes and must not need external services.
Do not rewrite the explanation.

Answer ONLY in Markdown, with exactly these two sections, in this order:

## Practice Exercise
- **Task**: what the student must write.
- **Expected input**: an example input (or "None" if not applicable).
- **Expected output**: the exact expected output (or "None").
- **Hint 1**: a small hint.
- **Hint 2**: a second hint (optional).

## Common Mistakes
A bullet list of 3 mistakes beginners often make with this topic.
"""

def create_practice_designer_agent():
    """Creer l'agent qui va te monter des execice de travail"""
    return Agent(
        name="practice_designer_agent",                                     # identifiant, sans espace
        model=get_model(),                                                  # le modèle via LiteLLM
        description="Designs a short practice exercise for a topic.",       # à quoi il sert (1 phrase)
        instruction=PRACTICE_INSTRUCTION,                                   # LE comportement
    )


async def run_practice_designer_agent(topic, explanation):
    """Run the Explainer Agent on a topic and return its Markdown."""
    agent = create_practice_designer_agent()
    prompt = (
        f"topic: {topic}\n\n"
        f"Explanation written by the explainer agent;\n{explanation}"
    )
    return await run_agent(agent, prompt)