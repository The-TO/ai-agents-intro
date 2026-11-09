"""Deterministic tool: save Markdown content to a file."""
from pathlib import Path

def save_markdown_file(file_path: str, content: str) -> str:
    """Write content to file_path and return a short result message."""
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)      # Ensure the parent directory exists.
        path.write_text(content, encoding="utf-8")          # Write the Markdown content.
    except OSError as error:
        return f"Error: could not write {path}: {error}"    # Return a useful message or the saved path.
    return f"Saved: {path}"