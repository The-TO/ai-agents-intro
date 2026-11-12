"""Deterministic tool: save Markdown content to a file."""
# Un "outil" est du Python normal : même entrée = même sortie.
# Aucun import de google.adk ici : on peut le tester sans agent.
from pathlib import Path

def save_markdown_file(file_path: str, content: str) -> str:
    """Write content to file_path and return a short result message."""
    # Path transforme la chaîne "output/study_guide.md" en objet chemin,
    # qui a des méthodes pratiques (.parent, .mkdir, .write_text...).
    path = Path(file_path)
    try:
        # path.parent est le dossier du fichier ("output").
        # parents=True crée aussi les dossiers intermédiaires ;
        # exist_ok=True : pas d'erreur si le dossier existe déjà.
        path.parent.mkdir(parents=True, exist_ok=True)
        # Écrit tout le texte d'un coup (et remplace l'ancien fichier).
        # utf-8 : les accents et emojis du modèle passent sans souci.
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        # OSError regroupe presque toutes les erreurs de fichier
        # (permission refusée, chemin invalide...). On renvoie un
        # message au lieu de planter : main.py décidera quoi faire.
        return f"Error: could not write {path}: {error}"
    # Pas d'erreur : on renvoie le chemin du fichier enregistré.
    return f"Saved: {path}"
