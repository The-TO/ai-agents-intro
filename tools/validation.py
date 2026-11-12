"""Deterministic tool: check that a study guide has every required section."""
# Le validateur vérifie la STRUCTURE (les titres sont-ils là ?),
# pas la qualité ni la vérité du contenu.

# Les 8 titres obligatoires, dans l'ordre de la fiche finale.
# Ils doivent correspondre aux titres demandés dans les instructions
# des agents (et "# Topic:" écrit par main.py).
REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def get_headings(markdown: str) -> list:
    """Return the text of every Markdown heading, in lowercase."""
    headings = []
    # Vaut True quand on est entre deux lignes ``` (bloc de code).
    in_code_block = False
    # splitlines() découpe le texte en une liste de lignes.
    for line in markdown.splitlines():
        # Enlève les espaces au début et à la fin de la ligne.
        line = line.strip()
        if line.startswith("```"):
            # A Python comment like "# loop" inside code is not a heading.
            # Chaque ``` ouvre ou ferme un bloc : on inverse le booléen.
            in_code_block = not in_code_block
        elif line.startswith("#") and not in_code_block:
            # "### Key Concepts" -> "Key Concepts" -> "key concepts".
            # lstrip('#') enlève TOUS les # du début : ## et ### sont
            # donc acceptés tous les deux.
            # lower() : la comparaison ignore les majuscules.
            headings.append(line.lstrip('#').strip().lower())
    return headings

def validate_required_sections(markdown: str) -> dict:
    """Return {'valid': bool, 'missing': [section names not found]}."""
    headings = get_headings(markdown)
    missing = []
    # Pour chaque section obligatoire...
    for section in REQUIRED_SECTIONS:
        found = False
        # ... on cherche un titre qui COMMENCE par son nom.
        # startswith accepte "topic: python decorators" pour "Topic",
        # mais refuse "explanation" pour "Simple Explanation".
        for heading in headings:
            if heading.startswith(section.lower()):
                found = True
                # Trouvé : inutile de regarder les titres suivants.
                break
        if not found:
            missing.append(section)
    # Le document est valide si aucune section ne manque.
    # Exemple : {"valid": False, "missing": ["Final Summary"]}
    return {"valid": len(missing) == 0, "missing": missing}