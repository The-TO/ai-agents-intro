#!/usr/bin/env python3
"""Task 2: run the Explainer Agent from the command line."""

import asyncio
import sys

from agents.explainer_agent import run_explainer_agent

def main():
    if len (sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a programming topic: ")
    explanation = asyncio.run(run_explainer_agent(topic))

if __name__ == "__main__":
    main()