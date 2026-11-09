"""Deterministic tool: check that a study guide has every required section."""
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


def get_headings(markdown str) -> list:
    """Return the text of every Markdown heading, in lowercase."""
    headings = []
    in_code_block = False
    for line in markdown.splitlines():
        line = line.strips()
        if line.startwith("```"):
            # A Python comment like "# loop" inside code is not a heading.
            in_code_block = not in_code_block
        elif line.startwith("#") and not in_code_block:
            headings.append(line.lstrip('#').strip().lower())
    return headings

def validate_required_sections(markdown: str) -> dict:
    """Return {'valid': bool, 'missing': [section names not found]}."""
    headings = get_headings(markdown)
    missing = []
    for section in REQUIRED_SECTIONS:
        found = False
        for heading in headings:
            if heading.startwith(section.lower()):
                found = True
                break
        if not found:
            missing.append(section)
    return {"valid": len(missing) == 0, "missing": missing}
