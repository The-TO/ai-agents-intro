"""Configuration helpers: read the .env file and check that Ollama is ready."""
# Ce fichier vérifie la configuration AVANT de lancer les agents.
# But : afficher un message clair ("Ollama ne tourne pas") au lieu
# d'une longue traceback illisible au milieu du workflow.

import json
import os
# urllib fait partie de la bibliothèque standard : il permet d'envoyer
# une requête HTTP sans rien installer (comme curl, mais en Python).
import urllib.error
import urllib.request

from dotenv import load_dotenv

# Lit le fichier .env (s'il existe) et copie chaque ligne VARIABLE=valeur
# dans os.environ. Ensuite, os.getenv("MODEL_NAME") peut la retrouver.
# Ce code s'exécute une seule fois, au premier "import config".
load_dotenv()


def get_model_name():
    """Return the LiteLLM model name, e.g. 'ollama_chat/llama3.2:3b'."""
    # os.getenv(nom, défaut) renvoie la valeur de la variable,
    # ou "" si elle n'existe pas (sans le défaut, ce serait None).
    # .strip() enlève les espaces : "  " est traité comme vide.
    model_name = os.getenv("MODEL_NAME", "").strip()
    if not model_name:
        # raise arrête la fonction et "remonte" l'erreur jusqu'au
        # try/except de main.py, qui affiche ce message.
        raise EnvironmentError(
            "MODEL_NAME is not set. Copy .env.example to .env "
            "and set MODEL_NAME (example: ollama_chat/llama3.2:3b)."
        )
    return model_name


def check_ollama(api_base, model_name):
    """Check that the Ollama server answers and that the model is pulled."""
    # LiteLLM veut "ollama_chat/llama3.2:3b", mais Ollama ne connaît
    # que "llama3.2:3b". split("/", 1) coupe une seule fois au "/",
    # et [1] garde la partie de droite.
    ollama_model = model_name.split("/", 1)[1]
    # Un modèle téléchargé sans taille s'appelle "nom:latest"
    # dans la liste d'Ollama : on ajoute ":latest" pour comparer.
    if ":" not in ollama_model:
        ollama_model += ":latest"

    try:
        # GET http://localhost:11434/api/tags renvoie, en JSON, la liste
        # des modèles téléchargés (comme "ollama list").
        # timeout=3 : on n'attend pas plus de 3 secondes.
        # "with" ferme la connexion automatiquement à la fin du bloc.
        with urllib.request.urlopen(api_base + "/api/tags", timeout=3) as resp:
            # json.load transforme la réponse JSON en dictionnaire Python.
            data = json.load(resp)
    except (urllib.error.URLError, OSError):
        # Connexion impossible = le serveur Ollama n'est pas lancé.
        # On remplace l'erreur technique par un message utile.
        raise ConnectionError(
            f"Cannot reach Ollama at {api_base}. "
            "Is it running? Start it with: ollama serve"
        )

    # data ressemble à {"models": [{"name": "llama3.2:3b", ...}, ...]}.
    # Cette liste en compréhension ne garde que les noms des modèles.
    # data.get("models", []) renvoie [] si la clé n'existe pas.
    available = [model["name"] for model in data.get("models", [])]
    if ollama_model not in available:
        raise EnvironmentError(
            f"Model '{ollama_model}' is not available in Ollama. "
            f"Download it with: ollama pull {ollama_model}"
        )


def check_config():
    """Run every configuration check before the agents start."""
    # Appelée une seule fois, au début de main().
    model_name = get_model_name()
    # On ne vérifie Ollama que si le modèle passe par Ollama.
    # Avec un autre fournisseur (gemini/..., openai/...), on saute
    # cette partie.
    if model_name.startswith("ollama"):
        api_base = os.getenv("OLLAMA_API_BASE", "").strip()
        if not api_base:
            raise EnvironmentError(
                "OLLAMA_API_BASE is not set. "
                "Add OLLAMA_API_BASE=http://localhost:11434 to your .env file."
            )
        check_ollama(api_base, model_name)
    # On renvoie le nom du modèle pour que main.py puisse l'afficher.
    return model_name
