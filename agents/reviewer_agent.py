"""Reviewer Agent: reviews a draft study guide and comments on it."""
from google.adk.agents import Agent

from agents.agent_runner import get_model, run_agent

# Le Reviewer fait du contrôle qualité : il COMMENTE le brouillon,
# il ne le réécrit pas ("Do NOT rewrite the guide").
# L'exemple utile / inutile ("The example does not show the function
# call" vs "Improve the explanation") montre au modèle le niveau de
# précision attendu : les modèles imitent bien les exemples.
# Il écrit aussi "## Final Summary", car c'est le seul agent qui a lu
# toute la fiche.
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
- Each suggestion must name a specific part of the guide.
- If you list missing information, recommend "Needs revision".

## Final Summary
Two or three sentences: what the student must remember about the topic.
"""

def create_reviewer_agent():
    """Creer le reviewer agent."""
    return Agent(
        # Identifiant de l'agent, sans espace.
        name="explainer_agent",
        # Le même modèle que les autres agents.
        model=get_model(),
        # À quoi sert l'agent, en une phrase.
        description="Reviews a draft study guide and gives feedback.",
        # Son comportement : l'instruction définie plus haut.
        instruction=REVIEWER_INSTRUCTION,
    )


# Le Reviewer reçoit UN seul paramètre : le brouillon complet
# (titre + explication + exercice), qui contient déjà le sujet.
async def run_reviewer_agent(draft):
    """Run the Reviewer Agent on a draft and return its comments."""
    agent = create_reviewer_agent()
    return await run_agent(agent, f"Draft study guide to review:\n\n{draft}")
