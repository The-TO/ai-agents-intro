#!/usr/bin/env python3
"""AI Study Guide Generator: runs the agents one after the other."""
import asyncio
import json
import sys
from pathlib import Path

from litellm.exceptions import APIConnectionError

from agents.explainer_agent import run_explainer_agent
from agents.practice_designer_agent import run_practice_designer_agent
from agents.reviewer_agent import run_reviewer_agent
from config import check_config
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

OUTPUT_PATH = "output/study_guide.md"
EXAMPLES_PATH = Path("data/topic_examples.json")


def load_example_topics():
    """Return the example topics from data/topic_examples.json."""
    try:
        with open(EXAMPLES_PATH, encoding="utf-8") as file:
            return json.load(file)["topics"]
    except (OSError, ValueError, KeyError):
        return []


def get_topic_from_user():
    """Read the topic from the command line, or ask for it."""
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        examples = load_example_topics()
        if examples:
            print("Examples: " + ", ".join(examples))
        topic = input("Enter a programming topic: ")
    if not topic.strip():
        raise ValueError("Topic cannot be empty.")
    return topic.strip()


def assemble_markdown(topic, explanation, practice):
    """Build the draft study guide (everything except the review)."""
    return f"# Topic: {topic}\n\n{explanation}\n\n{practice}\n"


def assemble_final_markdown(draft, review):
    """Add the review comments and final summary to the draft."""
    return f"{draft.rstrip()}\n\n{review}\n"


async def run_workflow(topic):
    """Run the three agents in order and return the final Markdown."""
    print("[1/3] Explainer agent is writing the explanation...")
    explanation = await run_explainer_agent(topic)

    print("[2/3] Practice designer agent is creating the exercise...")
    practice = await run_practice_designer_agent(topic, explanation)

    draft = assemble_markdown(topic, explanation, practice)

    print("[3/3] Reviewer agent is reviewing the draft...")
    review = await run_reviewer_agent(draft)

    return assemble_final_markdown(draft, review)


def main():
    """Entry point: check config, run the agents, validate, then save."""
    try:
        model_name = check_config()
        topic = get_topic_from_user()
    except (ValueError, EnvironmentError, ConnectionError) as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(f"Model: {model_name} | Topic: {topic}")
    try:
        final_markdown = asyncio.run(run_workflow(topic))
    except APIConnectionError as error:
        print(f"Error: lost the connection to the model: {error}")
        sys.exit(1)

    result = validate_required_sections(final_markdown)
    if result["valid"]:
        print("Validation: OK, all required sections are present.")
    else:
        print("Validation: FAILED. Missing sections: "
              + ", ".join(result["missing"]))

    message = save_markdown_file(OUTPUT_PATH, final_markdown)
    print(message)
    if message.startswith("Error") or not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()