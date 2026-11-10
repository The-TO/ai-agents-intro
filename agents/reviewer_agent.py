"""Reviewer Agent: reviews a draft study guide and comments on it."""
from google.adk.agents import Agent

from agents.agent_runner import get_model, run_agent

REVIEWER_INSTRUCTION = """You are a reviewer agent.
You receive the draft of a study guide written by other agents.
Review it for clarity, completeness and usefulness for a beginner.
Be critical but constructive. Be specific: "The example does not show
the function call" is useful, "Improve the explanation" is not.
Do NOT rewrite the guide.

Answer ONLY in Markdown, with exactly these two sections, in this order:

## Review Comments
- **Missing information**: what is missing (or "Nothing important").
- **Unclear parts**: what is ambiguous or unclear (or "None").
- **Suggestions**: 2 or 3 short, actionable improvements.
- **Recommendation**: "Approved" or "Needs revision", with one sentence why.

## Final Summary
Two or three sentences: what the student must remember about the topic.
"""

def create_reviewer_agent():
    """Creer le reviewer agent."""
    return Agent(
        name="explainer_agent",                                           # identifiant, sans espace
        model=get_model(),                                                # le modèle via LiteLLM
        description="Reviews a draft study guide and gives feedback.",    # à quoi il sert (1 phrase)
        instruction=REVIEWER_INSTRUCTION,                                 # LE comportement
    )


async def run_reviewer_agent(draft):
    """Run the Reviewer Agent on a draft and return its comments."""
    agent = create_reviewer_agent()
    return await run_agent(agent, f"Draft study guide to review:\n\n{draft}")