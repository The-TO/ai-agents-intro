#!/usr/bin/env python3
"""AI Study Guide Generator: runs the agents one after the other."""
# Point d'entrée du projet. Se lance depuis la racine du projet :
#     python3 main.py "Python decorators"
import asyncio
import json
import sys
from pathlib import Path

# L'exception levée par LiteLLM quand il perd la connexion au modèle.
from litellm.exceptions import APIConnectionError

# Les trois agents (le modèle, non déterministe)...
from agents.explainer_agent import run_explainer_agent
from agents.practice_designer_agent import run_practice_designer_agent
from agents.reviewer_agent import run_reviewer_agent
from config import check_config
# ... et les deux outils (du code Python, déterministe).
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

# Constantes en MAJUSCULES : des valeurs fixes, définies une seule fois.
OUTPUT_PATH = "output/study_guide.md"
EXAMPLES_PATH = Path("data/topic_examples.json")


def load_example_topics():
    """Return the example topics from data/topic_examples.json."""
    try:
        with open(EXAMPLES_PATH, encoding="utf-8") as file:
            # json.load renvoie {"topics": [...]} : on garde la liste.
            return json.load(file)["topics"]
    # OSError : fichier absent ; ValueError : JSON invalide ;
    # KeyError : pas de clé "topics". Dans tous les cas, ce n'est
    # qu'un bonus d'affichage : on renvoie une liste vide sans planter.
    except (OSError, ValueError, KeyError):
        return []


def get_topic_from_user():
    """Read the topic from the command line, or ask for it."""
    # sys.argv = ["main.py", "Python", "decorators"] si on tape
    # python3 main.py Python decorators (sans guillemets).
    # sys.argv[1:] enlève "main.py", " ".join recolle les mots.
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        # Pas d'argument : on montre des idées puis on demande.
        examples = load_example_topics()
        if examples:
            print("Examples: " + ", ".join(examples))
        topic = input("Enter a programming topic: ")
    # On refuse un sujet vide ou fait seulement d'espaces.
    if not topic.strip():
        raise ValueError("Topic cannot be empty.")
    return topic.strip()


def assemble_markdown(topic, explanation, practice):
    """Build the draft study guide (everything except the review)."""
    # Le titre "# Topic:" est écrit par NOTRE code, pas par un agent :
    # cette section ne peut donc jamais manquer.
    # \n\n = retour à la ligne + ligne vide : en Markdown, la ligne
    # vide sépare les blocs (sinon un titre peut se coller au texte).
    return f"# Topic: {topic}\n\n{explanation}\n\n{practice}\n"


def assemble_final_markdown(draft, review):
    """Add the review comments and final summary to the draft."""
    # rstrip() enlève les retours à la ligne en fin de brouillon,
    # pour ne pas empiler des lignes vides avant la review.
    return f"{draft.rstrip()}\n\n{review}\n"


# Orchestration séquentielle : chaque étape utilise le résultat de la
# précédente. "await" attend qu'un agent ait fini avant de passer au
# suivant.
async def run_workflow(topic):
    """Run the three agents in order and return the final Markdown."""
    print("[1/3] Explainer agent is writing the explanation...")
    explanation = await run_explainer_agent(topic)

    # Le Practice Designer reçoit la sortie de l'Explainer.
    print("[2/3] Practice designer agent is creating the exercise...")
    practice = await run_practice_designer_agent(topic, explanation)

    draft = assemble_markdown(topic, explanation, practice)

    # Le Reviewer reçoit tout le brouillon.
    print("[3/3] Reviewer agent is reviewing the draft...")
    review = await run_reviewer_agent(draft)

    return assemble_final_markdown(draft, review)


def main():
    """Entry point: check config, run the agents, validate, then save."""
    # Étape 1 : vérifier la config et le sujet AVANT les agents.
    # On attrape seulement les erreurs prévues ; une erreur imprévue
    # garde sa traceback complète, utile pour déboguer.
    try:
        model_name = check_config()
        topic = get_topic_from_user()
    except (ValueError, EnvironmentError, ConnectionError) as error:
        print(f"Error: {error}")
        # Code de sortie 1 = "échec" pour le terminal (echo $? -> 1).
        sys.exit(1)

    print(f"Model: {model_name} | Topic: {topic}")
    # Étape 2 : lancer les agents. asyncio.run démarre la partie
    # asynchrone depuis du code normal, une seule fois.
    try:
        final_markdown = asyncio.run(run_workflow(topic))
    except APIConnectionError as error:
        # Ex. : Ollama arrêté pendant la génération.
        print(f"Error: lost the connection to the model: {error}")
        sys.exit(1)

    # Étape 3 : valider la structure avec l'outil déterministe.
    result = validate_required_sections(final_markdown)
    if result["valid"]:
        print("Validation: OK, all required sections are present.")
    else:
        print("Validation: FAILED. Missing sections: "
              + ", ".join(result["missing"]))

    # Étape 4 : sauvegarder. On enregistre même si la validation
    # échoue, pour pouvoir ouvrir le fichier et voir ce qui manque.
    message = save_markdown_file(OUTPUT_PATH, final_markdown)
    print(message)
    if message.startswith("Error") or not result["valid"]:
        sys.exit(1)


# Ce bloc ne s'exécute que si on lance "python3 main.py" directement,
# pas si un autre fichier fait "import main".
if __name__ == "__main__":
    main()
