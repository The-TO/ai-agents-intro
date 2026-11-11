# AI Agents in Python

## Description

An **AI Study Guide Generator** built with Google ADK, LiteLLM and Ollama.

You give it a programming topic (for example `Python decorators`). Three
agents with separate responsibilities run one after the other on a model
that runs locally, then two deterministic Python tools validate and save the
result as a Markdown study guide in `output/study_guide.md`.

```text
Topic → Explainer Agent → Practice Designer Agent → Reviewer Agent
      → validate_required_sections() → save_markdown_file() → study_guide.md
```

The generated guide always contains these sections:
Topic, Simple Explanation, Key Concepts, Example, Practice Exercise,
Common Mistakes, Review Comments, Final Summary.

## Requirements

- Python 3.10 or newer (tested with Python 3.12 on macOS and 3.14 on WSL)
- [Ollama](https://ollama.com) installed and running
- The local model `llama3.2:3b` (about 2 GB) pulled with Ollama
- macOS, Linux, or Windows with WSL (Ubuntu)
- About 4 GB of free RAM while the model runs

Python dependencies (`requirements.txt`):

| Package | Role |
|---------|------|
| `google-adk` | Defines and runs the agents (`Agent`, `Runner`, sessions) |
| `litellm` | Connects ADK to the model provider (here Ollama) |
| `python-dotenv` | Loads the variables of the `.env` file |

Tested on:

- MacBook Pro, Apple M5 (Ollama uses the GPU through Metal)
- Windows PC with WSL (Ubuntu), Ollama installed inside WSL

## Setup

```bash
git clone https://github.com/The-TO/ai-agents-intro.git
cd ai-agents-intro

# 1. Virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Ollama
#    macOS: install the app from https://ollama.com/download
#           (or: brew install ollama)
#    WSL:   curl -fsSL https://ollama.com/install.sh | sh

# 3. Model
ollama pull llama3.2:3b
ollama list                                         # llama3.2:3b is listed
ollama run llama3.2:3b "Say hello in one sentence." # quick test
```

On WSL, if `python3 -m venv` fails, install it first:
`sudo apt install python3-venv`.

Ollama usually starts by itself (the macOS app, or the systemd service on
WSL). Check that it answers with:

```bash
curl http://localhost:11434
# Ollama is running
```

## Configuration

Copy the example file, then adapt the values if needed:

```bash
cp .env.example .env
```

| Variable | Example | Meaning |
|----------|---------|---------|
| `OLLAMA_API_BASE` | `http://localhost:11434` | Address of the Ollama server |
| `MODEL_NAME` | `ollama_chat/llama3.2:3b` | LiteLLM model name: `ollama_chat/` + the name shown by `ollama list` |

**Model provider:** Ollama (local), reached through LiteLLM with the
`ollama_chat` provider. No API key is needed.

`.env` is listed in `.gitignore` and is never committed: only
`.env.example` (variable names, no secrets) is in the repository.

To use another LiteLLM provider (Gemini, OpenAI, Claude...), set
`MODEL_NAME` to that provider's model string (for example
`gemini/gemini-2.0-flash`) and add the provider's API key variable to your
local `.env` only. The Ollama checks are skipped when `MODEL_NAME` does not
start with `ollama`.

## How to Run

Always run the project **from the root folder** `ai-agents-intro/`, with the
virtual environment activated and Ollama running:

```bash
python3 main.py "Python decorators"
```

Without an argument, the program shows the example topics from
`data/topic_examples.json` and asks for one:

```text
$ python3 main.py
Examples: Python decorators, Python list comprehensions, HTTP status codes
Enter a programming topic:
```

The program exits with code `0` when the guide is valid and saved, and with
code `1` when something fails (configuration, connection, validation or
file writing).

## Example Input

```bash
python3 main.py "Python decorators"
```

## Example Output

Terminal:

```text
Model: ollama_chat/llama3.2:3b | Topic: Python decorators
[1/3] Explainer agent is writing the explanation...
[2/3] Practice designer agent is creating the exercise...
[3/3] Reviewer agent is reviewing the draft...
Validation: OK, all required sections are present.
Saved: output/study_guide.md
```

Extract of `output/study_guide.md` (shortened):

```markdown
# Topic: Python decorators

### Simple Explanation
Python decorators are a powerful tool for modifying the behavior of
functions without changing their source code. [...]

### Key Concepts
- **Function wrapper**: a function that takes another function as an
  argument and returns a new function that "wraps" the original function.
[...]

## Practice Exercise
- **Task**: write a decorator that logs the execution time of a function.
- **Expected input**: None
- **Hint 1**: use the `time` module to measure execution time.
[...]

## Review Comments
- **Unclear parts**: The explanation of the decorator return value is not
  clear.
- **Recommendation**: Needs revision

## Final Summary
Students should remember that decorators are a powerful tool for modifying
function behavior without changing source code [...]
```

The full generated file is in [`output/study_guide.md`](output/study_guide.md).

## Project Structure

```text
ai-agents-intro/
├── agents/
│   ├── __init__.py
│   ├── agent_runner.py            # shared get_model() + run_agent()
│   ├── explainer_agent.py         # Explainer Agent
│   ├── practice_designer_agent.py # Practice Designer Agent
│   └── reviewer_agent.py          # Reviewer Agent
├── tools/
│   ├── __init__.py
│   ├── file_writer.py             # save_markdown_file()
│   └── validation.py              # validate_required_sections()
├── output/
│   └── study_guide.md             # generated study guide
├── data/
│   └── topic_examples.json        # example topics shown to the user
├── config.py                      # reads .env, checks Ollama and the model
├── main.py                        # sequential workflow (entry point)
├── .env.example                   # documented variables, no secrets
├── .gitignore
├── requirements.txt
└── README.md
```

`agents/agent_runner.py` and `config.py` are not required by the project
structure. They avoid copying the same agent-running code into the three
agents, and keep the configuration checks out of `main.py`.

## Agents

Each agent has one responsibility. Information passes from one agent to the
next **through the prompt**: each agent has its own session and does not see
what the other agents wrote unless it is included in its message.

| Agent | Receives | Produces | Must not |
|-------|----------|----------|----------|
| Explainer (`explainer_agent`) | the topic | `Simple Explanation`, `Key Concepts`, `Example` | add other sections |
| Practice Designer (`practice_designer_agent`) | the topic + the explanation | `Practice Exercise` (task, expected input/output, hints), `Common Mistakes` | rewrite the explanation |
| Reviewer (`reviewer_agent`) | the full draft | `Review Comments` (missing info, unclear parts, suggestions, recommendation), `Final Summary` | rewrite the guide |

The `# Topic:` title is written by `main.py`, not by an agent, so it can
never be missing.

## Tools

| Tool | Input | Output |
|------|-------|--------|
| `save_markdown_file(file_path, content)` | a path and Markdown text | `"Saved: <path>"`, or `"Error: could not write ..."`; creates the parent folder if needed |
| `validate_required_sections(markdown)` | Markdown text | `{"valid": bool, "missing": [...]}` |

Both tools are plain Python, independent from Google ADK: same input, same
output, every time. They can be tested without any agent:

```bash
python3 -c "from tools.file_writer import save_markdown_file as s; print(s('output/test.md', '# Hello'))"
```

```python
>>> from tools.validation import validate_required_sections as v
>>> v("# Topic: X\n## Explanation\n## Example\n")
{'valid': False, 'missing': ['Simple Explanation', 'Key Concepts', 'Practice Exercise', 'Common Mistakes', 'Review Comments', 'Final Summary']}
```

The validator reads only Markdown headings, ignores lines inside code blocks
(a Python comment such as `# Example` is not a heading), ignores case, and
accepts `##` as well as `###`.

## Self-Validation Checklist

**Task 0: Project structure**
- [x] I created the required project directories.
- [x] I created README.md, requirements.txt, .env.example, .gitignore and main.py.
- [x] My project structure is easy to understand.

**Task 1: Local model environment**
- [x] I created and activated a Python virtual environment.
- [x] I installed the required Python dependencies.
- [x] I installed Ollama and pulled a small local model.
- [x] I confirmed that the model responds locally.
- [x] I documented the setup process and the model I used in README.md.
- [x] I did not commit secrets or local environment files.

**Task 2: Explainer Agent**
- [x] I created agents/explainer_agent.py.
- [x] The agent produces an explanation, key concepts and one example.
- [x] I can run the agent from main.py.
- [x] I tested the agent with at least two topics.

**Task 3: File writer tool**
- [x] I created tools/file_writer.py and implemented save_markdown_file().
- [x] The function receives a path and Markdown content and writes the file.
- [x] I tested the function without using the agent.
- [x] I used the function to save agent output in the output directory.

**Task 4: Validation tool**
- [x] I created tools/validation.py and implemented validate_required_sections().
- [x] The function checks for all required sections and reports missing ones.
- [x] I tested the function with valid and with incomplete Markdown.
- [x] I used the validator in the project workflow.

**Task 5: Practice Designer Agent**
- [x] I created agents/practice_designer_agent.py.
- [x] The agent has a clear and separate responsibility.
- [x] The agent receives the topic and the previous explanation.
- [x] The agent generates a practice exercise with hints.

**Task 6: Reviewer Agent**
- [x] I created agents/reviewer_agent.py.
- [x] The agent reviews an existing draft and identifies missing or unclear parts.
- [x] The agent provides suggestions for improvement.
- [x] The agent does not replace the other agents.
- [x] The review comments are included in the final Markdown file.

**Task 7: Sequential workflow**
- [x] main.py runs the full workflow in order.
- [x] The Practice Designer Agent uses the previous output.
- [x] The Reviewer Agent reviews the draft.
- [x] The final Markdown file includes all required sections.
- [x] Missing sections are reported clearly.
- [x] The final file is saved in output/study_guide.md.

**Task 8: Error handling and configuration**
- [x] The project checks for empty topic input.
- [x] The project handles file-writing errors.
- [x] The project reports validation failures clearly.
- [x] The README includes troubleshooting notes and explains how to configure the model provider.
- [x] The project does not expose secrets.

**Task 9: README**
- [x] README.md includes all required sections, an example input and output,
  the agents, the tools, a reflection and known limitations.

## Reflection

1. **What is the difference between a direct LLM call and an AI agent?**
   A direct call sends one prompt to a model and gets one text back, with
   nothing around it. An agent wraps the model with a name, a role, fixed
   instructions, optional tools and execution logic (a `Runner` and a
   session in Google ADK). The instructions apply to every message, so the
   agent behaves the same way each time it is used, can be tested on its
   own, and can be combined with other agents in a workflow.

2. **What role does each agent have in your system?**
   The Explainer Agent teaches the topic (explanation, key concepts,
   example). The Practice Designer Agent turns that explanation into one
   small exercise and lists common mistakes. The Reviewer Agent reads the
   whole draft, comments on it without rewriting it, and writes the final
   summary. Each agent has one job, so their outputs do not repeat each
   other.

3. **What role does each tool have in your system?**
   `save_markdown_file()` writes the guide to `output/study_guide.md` and
   returns a clear message if writing fails. `validate_required_sections()`
   checks that the eight required headings are present and lists the
   missing ones. The model is used for flexible text generation; the tools
   handle the parts that must be reliable, because they are deterministic.

4. **What was the most difficult part of the project?**
   Most of my problems were not in the agent logic but in the setup and in
   small Python errors. My first runs failed because I had no `.env` file
   (`os.getenv("MODEL_NAME")` returned `None`, which gave an unclear
   pydantic error), because I launched `main.py` from the `agents/` folder
   instead of the project root, and because of syntax mistakes such as a
   missing comma or passing `get_model` instead of `get_model()`. I also had
   to understand the asynchronous part of ADK (`async`, `await`,
   `asyncio.run` and the `async for` loop over the runner events). These
   problems are the reason why `config.py` checks the configuration before
   any agent runs.

5. **What limitation did you observe when using your selected model?**
   With `llama3.2:3b`, the format instructions are followed only
   approximately: the Explainer writes `### Simple Explanation` instead of
   the requested `## Simple Explanation`, so the validator had to accept any
   number of `#`. The content is also not always reliable: in one run, the
   exercise was an exact copy of the example with its solution included,
   and one "common mistake" was factually wrong ("forgetting to return the
   original function", while a decorator must return the wrapper). In
   another run, the key concepts gave a wrong decorator syntax
   (`@decorator_name(func_name)`). The Reviewer does not detect these
   factual errors, and once recommended "Approved" while listing missing
   information. Each agent takes several seconds to answer, so a full run
   takes noticeably longer than a single call.

## Known Limitations

- **Headings are not always respected:** the model sometimes uses `###`
  instead of `##`. The validator accepts it, but a renamed heading
  (for example `Explanation` instead of `Simple Explanation`) makes the
  validation fail.
- **Hallucinations:** the model can state wrong facts with confidence
  (for example a wrong decorator syntax in *Key Concepts*). Nothing in the
  system checks facts: the validator only checks the structure.
- **The Reviewer is not a fact checker:** it comments on structure and
  clarity, misses factual errors, and its recommendation is not always
  consistent with its own comments.
- **Exercise quality varies:** the exercise can repeat the example, include
  its own solution, or give a vague expected output.
- **Different output on each run:** the same topic gives a different guide
  every time.
- **No automatic correction:** when the Reviewer recommends "Needs
  revision" or the validation fails, the guide is still saved as it is; the
  agents are not run again.
- **Speed depends on the hardware:** three agents run one after the other,
  each one taking several seconds; it is slower on a machine without a GPU.
- **Small model:** a larger model (for example `qwen2.5:7b`) would probably
  follow the format better, but needs more RAM and is slower.

## Troubleshooting

| Message | Cause | Fix |
|---------|-------|-----|
| `MODEL_NAME is not set` | No `.env` file, or variable missing | `cp .env.example .env` |
| `OLLAMA_API_BASE is not set` | Variable missing in `.env` | Add `OLLAMA_API_BASE=http://localhost:11434` |
| `Cannot reach Ollama at ...` | Ollama is not running | Open the Ollama app (macOS) or run `ollama serve` |
| `Model '...' is not available` | Model not pulled, or typo in `MODEL_NAME` | `ollama pull <model>` and compare with `ollama list` |
| `Topic cannot be empty.` | Empty topic | `python3 main.py "HTTP status codes"` |
| `Error: could not write ...` | No permission on the output folder | Check the folder permissions |
| `Validation: FAILED. Missing sections: ...` | The model renamed or skipped a heading | Run again, or make the agent instruction stricter |
| `Error: lost the connection to the model` | Ollama stopped during generation | Restart Ollama and run again |
| `ollama serve` → `bind: address already in use` | Ollama is **already running** (app or service) | Nothing to do: do not start it a second time |
| `can't open file '.../agents/main.py'` | Command launched from a subfolder | `cd` back to the project root |
| `ModuleNotFoundError: No module named 'google.adk'` | Virtual environment not activated | `source .venv/bin/activate` |

On WSL, do not run Ollama both on Windows and inside WSL: both would use
port 11434. Keep only the WSL version.