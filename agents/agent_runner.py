"""Shared code for every agent: build the model and run an agent."""
# Ce fichier contient le code commun aux 3 agents. Sans lui, les
# ~25 lignes de run_agent() seraient copiées dans chaque agent.

# LiteLlm : le connecteur entre ADK et le modèle (ici via Ollama).
from google.adk.models.lite_llm import LiteLlm
# Runner : l'objet qui exécute un agent (envoie le message, gère les
# appels d'outils, produit des événements).
from google.adk.runners import Runner
# InMemorySessionService : garde l'historique des conversations en
# mémoire vive (perdu à la fin du programme, suffisant ici).
from google.adk.sessions import InMemorySessionService
# types : les classes de message (Content, Part) attendues par ADK.
from google.genai import types

from config import get_model_name

# Constantes utilisées par ADK pour ranger les sessions.
# Leur valeur exacte n'a pas d'importance, elles doivent juste être
# identiques pour le Runner et pour create_session.
APP_NAME = "study_guide_generator"
USER_ID = "student"


def get_model():
    """Build the LiteLLM connector from the MODEL_NAME variable."""
    # Exemple : LiteLlm(model="ollama_chat/llama3.2:3b").
    # Le préfixe "ollama_chat/" dit à LiteLLM de parler à Ollama ;
    # l'adresse d'Ollama est lue dans la variable OLLAMA_API_BASE.
    return LiteLlm(model=get_model_name())


# "async def" : fonction asynchrone. Elle s'appelle avec
# "await run_agent(...)" depuis une autre fonction async.
async def run_agent(agent, prompt):
    """Send one message to an agent and return its final text answer."""
    # 1. Le service qui stocke les sessions (conversations).
    session_service = InMemorySessionService()

    # 2. Le Runner : il relie l'agent et le service de sessions.
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # 3. Une nouvelle session = une nouvelle conversation, vide.
    # Chaque appel de run_agent repart de zéro : un agent ne voit
    # jamais ce qu'ont dit les autres agents, sauf si on le met
    # dans son prompt.
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # 4. ADK n'accepte pas une simple chaîne : le message est un objet
    # Content, avec un rôle ("user") et une liste de morceaux (Part).
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    # 5. run_async renvoie les événements un par un pendant que l'agent
    # travaille (réponses, appels d'outils...). "async for" les
    # parcourt au fur et à mesure qu'ils arrivent.
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        # On ne garde que la réponse finale de l'agent.
        # "and event.content" évite une erreur si l'événement est vide.
        if event.is_final_response() and event.content:
            # "or []" : si parts vaut None, on boucle sur une liste vide.
            parts = event.content.parts or []
            # On recolle le texte de tous les morceaux.
            # "part.text or ''" remplace un morceau sans texte par "".
            final_text = "".join(part.text or "" for part in parts)

    # Un modèle qui ne répond rien ne doit pas passer inaperçu.
    if not final_text.strip():
        raise RuntimeError(f"{agent.name} returned an empty answer.")
    return final_text.strip()