"""Configuration helpers: read the .env file and check that Ollama is ready."""
import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

# Read the .env file (if it exists) and put its values in os.environ.
load_dotenv()


def get_model_name():
    """Return the LiteLLM model name, e.g. 'ollama_chat/llama3.2:3b'."""
    model_name = os.getenv("MODEL_NAME", "").strip()
    if not model_name:
        raise EnvironmentError(
            "MODEL_NAME is not set. Copy .env.example to .env "
            "and set MODEL_NAME (example: ollama_chat/llama3.2:3b)."
        )
    return model_name


def check_ollama(api_base, model_name):
    """Check that the Ollama server answers and that the model is pulled."""
    # 'ollama_chat/llama3.2:3b' -> 'llama3.2:3b'
    ollama_model = model_name.split("/", 1)[1]
    if ":" not in ollama_model:
        ollama_model += ":latest"

    try:
        with urllib.request.urlopen(api_base + "/api/tags", timeout=3) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, OSError):
        raise ConnectionError(
            f"Cannot reach Ollama at {api_base}. "
            "Is it running? Start it with: ollama serve"
        )

    available = [model["name"] for model in data.get("models", [])]
    if ollama_model not in available:
        raise EnvironmentError(
            f"Model '{ollama_model}' is not available in Ollama. "
            f"Download it with: ollama pull {ollama_model}"
        )


def check_config():
    """Run every configuration check before the agents start."""
    model_name = get_model_name()
    if model_name.startswith("ollama"):
        api_base = os.getenv("OLLAMA_API_BASE", "").strip()
        if not api_base:
            raise EnvironmentError(
                "OLLAMA_API_BASE is not set. "
                "Add OLLAMA_API_BASE=http://localhost:11434 to your .env file."
            )
        check_ollama(api_base, model_name)
    return model_name