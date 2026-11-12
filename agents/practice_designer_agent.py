"""Practice Designer Agent: creates a small exercise from an explanation."""
from google.adk.agents import Agent

from agents.agent_runner import get_model, run_agent

# Cet agent a UNE responsabilité : créer un exercice. Il ne doit pas
# réexpliquer le sujet ("Do not rewrite the explanation").
# Le format en liste (- **Task**:, - **Expected input**:...) aide un
# petit modèle à ne rien oublier. Les "or None" évitent qu'il invente
# une entrée/sortie quand le sujet n'en a pas (ex. HTTP status codes).
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

# Même structure que l'Explainer : une fonction qui crée l'agent...
def create_practice_designer_agent():
    """Creer l'agent qui va te monter des execice de travail"""
    return Agent(
        # Identifiant de l'agent, sans espace.
        name="practice_designer_agent",
        # Le même modèle que les autres agents.
        model=get_model(),
        # À quoi sert l'agent, en une phrase.
        description="Designs a short practice exercise for a topic.",
        # Son comportement : l'instruction définie plus haut.
        instruction=PRACTICE_INSTRUCTION,
    )


# ... et une fonction qui le lance. Elle reçoit DEUX informations :
# le sujet et l'explication produite par l'Explainer Agent.
async def run_practice_designer_agent(topic, explanation):
    """Run the Explainer Agent on a topic and return its Markdown."""
    agent = create_practice_designer_agent()
    # C'est ici que l'information passe d'un agent à l'autre : on
    # copie l'explication DANS le prompt. Les agents ne partagent pas
    # de mémoire, chacun a sa propre session.
    # Deux f-strings côte à côte entre parenthèses sont collées
    # automatiquement par Python en une seule chaîne.
    prompt = (
        f"topic: {topic}\n\n"
        f"Explanation written by the explainer agent;\n{explanation}"
    )
    return await run_agent(agent, prompt)