# AI Agents in Python

## Description

An **AI Study Guide Generator** built with Google ADK, LiteLLM and Ollama.
You give it a programming topic (for example `Python decorators`) and three
agents work one after the other to produce a Markdown study guide, saved in
`output/study_guide.md`. Two deterministic Python tools validate and save
the result.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com) installed and running
- A local model pulled with Ollama (this project uses `llama3.2:3b`, about 2 GB)
- macOS, Linux, or Windows with WSL (Ubuntu)
- About 4 GB of free RAM while the model runs

## Setup

```bash
git clone <your-repo-url>
cd ai-agents-intro

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ollama pull llama3.2:3b
ollama run llama3.2:3b "Say hello in one sentence."   # quick test
```

On WSL, if `python3 -m venv` fails, install it first:
`sudo apt install python3-venv`.

## Configuration

Copy the example file and adapt it:

```bash
cp .env.example .env
```

| Variable | Example | Meaning |
|----------|---------|---------|
| `OLLAMA_API_BASE` | `http://localhost:11434` | Address of the Ollama server |
| `MODEL_NAME` | `ollama_chat/llama3.2:3b` | LiteLLM model name: `ollama_chat/` + the name shown by `ollama list` |

**Model provider:** Ollama (local), reached through LiteLLM with the
`ollama_chat` provider. No API key is needed. `.env` is listed in
`.gitignore` and is never committed.

To use another LiteLLM provider (Gemini, OpenAI, Claude...), set `MODEL_NAME`
to that provider's model string (for example `gemini/gemini-2.0-flash`) and add
the provider's API key variable to your local `.env` only.

## How to Run

Make sure Ollama is running (`ollama serve`, or the Ollama app on macOS), then:

```bash
python3 main.py "Python decorators"
```

Without an argument, the program shows example topics from
`data/topic_examples.json` and asks for one.

## Example Input

```text
python3 main.py "Python list comprehensions"
```

## Example Output

Terminal:

```text
Model: ollama_chat/llama3.2:3b | Topic: Python list comprehensions
[1/3] Explainer agent is writing the explanation...
[2/3] Practice designer agent is creating the exercise...
[3/3] Reviewer agent is reviewing the draft...
Validation: OK, all required sections are present.
Saved: output/study_guide.md
```

Start of `output/study_guide.md`:

```markdown
# Topic: Python list comprehensions

## Simple Explanation
A list comprehension is a short way to build a new list from another one...

## Key Concepts
- **Expression**: what to put in the new list.
...
```

## Project Structure

```text
ai-agents-intro/
├── agents/
│   ├── agent_runner.py            # shared model + run_agent() helper
│   ├── explainer_agent.py
│   ├── practice_designer_agent.py
│   └── reviewer_agent.py
├── tools/
│   ├── file_writer.py             # save_markdown_file()
│   └── validation.py              # validate_required_sections()
├── output/study_guide.md          # generated guide
├── data/topic_examples.json       # example topics
├── config.py                      # reads .env, checks Ollama
├── main.py                        # sequential workflow
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Agents

| Agent | Input | Output |
|-------|-------|--------|
| Explainer | the topic | Simple Explanation, Key Concepts, Example |
| Practice Designer | the topic + the explanation | Practice Exercise (with input, output, hints), Common Mistakes |
| Reviewer | the full draft | Review Comments (missing, unclear, suggestions, recommendation), Final Summary |

## Tools

| Tool | What it does |
|------|--------------|
| `save_markdown_file(file_path, content)` | Creates the parent folder if needed, writes the file, returns `Saved: <path>` or an `Error: ...` message. |
| `validate_required_sections(markdown)` | Reads the Markdown headings (ignoring code blocks) and returns `{"valid": bool, "missing": [...]}`. |

Both tools are plain Python: same input, same output, every time.

## Self-Validation Checklist

- [x] Project structure created (task 0)
- [x] Virtual environment, dependencies, Ollama and model working (task 1)
- [x] Explainer Agent runs from `main.py` (task 2)
- [x] `save_markdown_file()` tested alone and used in the workflow (task 3)
- [x] `validate_required_sections()` tested with valid and incomplete Markdown (task 4)
- [x] Practice Designer Agent uses the explanation (task 5)
- [x] Reviewer Agent comments without rewriting (task 6)
- [x] Full sequential workflow saves `output/study_guide.md` (task 7)
- [x] Common errors handled with clear messages (task 8)
- [x] README complete (task 9)

## Troubleshooting

| Message | Cause | Fix |
|---------|-------|-----|
| `MODEL_NAME is not set` | No `.env` file, or variable missing | `cp .env.example .env` |
| `Cannot reach Ollama at ...` | Ollama is not running | `ollama serve` (or open the Ollama app) |
| `Model '...' is not available` | Model not pulled, or typo in `MODEL_NAME` | `ollama pull <model>` and compare with `ollama list` |
| `Topic cannot be empty.` | Empty topic | Give a topic: `python3 main.py "HTTP status codes"` |
| `Error: could not write ...` | No permission on `output/` | Check folder permissions |
| `Validation: FAILED. Missing sections: ...` | The model changed or skipped a heading | Run again, or make the instruction stricter |
| `ModuleNotFoundError: google.adk` | venv not activated | `source .venv/bin/activate` |

## Reflection

1. **Direct LLM call vs agent:** a direct call sends one prompt and gets one
   answer. An agent wraps the model with a role, instructions, optional tools
   and execution logic (a runner, a session), so it behaves the same way
   every time it is used and can be combined with other agents.
2. **Agents:** the Explainer teaches the topic, the Practice Designer turns
   the explanation into a small exercise, the Reviewer checks the draft and
   writes the final summary. Each one has one job.
3. **Tools:** `save_markdown_file()` writes the guide to disk;
   `validate_required_sections()` checks the structure. They are
   deterministic, so they are reliable where the model is not.
4. **Most difficult part:** *(write your own answer)*
5. **Model limitation:** *(write what you observed, e.g. headings sometimes
   renamed, made-up details, slow answers on CPU)*

## Known Limitations

- A small local model can rename or skip a heading; validation then fails.
- The model can invent details (hallucinations); the reviewer does not
  verify facts.
- The output changes between runs for the same topic.
- Generation can take a minute or more on a machine without a GPU.
- Validation only checks the structure, not the quality of the content.