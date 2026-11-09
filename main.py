#!/usr/bin/env python3
"""Task 4: generate, validate, then save."""

import asyncio
import sys

from agents.explainer_agent import run_explainer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

OUTPUT_PATH = "output/study_guide.md"

def main():
    if len (sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a programming topic: ")
    explanation = asyncio.run(run_explainer_agent(topic))
    markdown = f"# Topic {topic}\n\n{explanation}\n"

    result = validate_required_sections
    if result["valid"]:
        print("Validation: OK")
    else:
        print("Validation: missing sections:" + ", ".join(result["missing"]))

    print(save_markdown_file(OUTPUT_PATH, markdown))

if __name__ == "__main__":
    main()