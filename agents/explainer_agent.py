"""Explainer Agent: explains a programming topic for beginners."""
from google.adk.agents import Agent

from agents.agent_runner import get_model, run_agent

# L'instruction est la partie la plus importante d'un agent : c'est
# elle qui transforme un modèle généraliste en "explainer".
# Les titres écrits ici (## Simple Explanation, ## Key Concepts,
# ## Example) doivent correspondre EXACTEMENT à REQUIRED_SECTIONS
# dans tools/validation.py, sinon la validation échoue.
# Les triples guillemets permettent une chaîne sur plusieurs lignes.
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

# On crée l'agent dans une fonction plutôt que dans une variable
# globale : l'agent n'est construit qu'au moment où on en a besoin,
# APRÈS les vérifications de config.py.
def create_explainer_agent():
    """Creer l'agent qui explique"""
    return Agent(
        # name : identifiant de l'agent, sans espace.
        name="explainer_agent",
        # model : l'objet LiteLlm (attention aux parenthèses : on veut
        # ce que get_model() renvoie, pas la fonction elle-même).
        model=get_model(),
        # description : à quoi sert l'agent, en une phrase.
        description="Explains a programming topic.",
        # instruction : le comportement de l'agent (voir plus haut).
        instruction=EXPLAINER_INSTRUCTION,
    )


async def run_explainer_agent(topic):
    """Run the Explainer Agent on a topic and return its Markdown."""
    agent = create_explainer_agent()
    # Le sujet va dans le PROMPT (le message), pas dans l'instruction :
    # l'instruction est fixe, le prompt change à chaque lancement.
    return await run_agent(agent, f"Topic: {topic}")