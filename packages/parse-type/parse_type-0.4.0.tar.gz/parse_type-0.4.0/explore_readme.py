#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import inspect
import doctest
import re

HERE = os.path.dirname(__file__)
README = os.path.join(HERE, "README.rst")

PATTERN = "^\.\. code-block:: python"
def extract_examples(doc):
    matcher = re.compile(PATTERN)
    examples = []
    current_example_lines = []
    state = "hunt"
    for index, line in enumerate(doc.splitlines()):
        if state == "hunt":
            if matcher.match(line):
                assert not current_example_lines
                state = "collect"
        elif state == "collect":
            if line.startswith("  ") or line.startswith("\t") or not line:
                current_example_lines.append(line)
            else:
                example = "\n".join(current_example_lines)
                examples.append(example.rstrip())

def main():
    pass

if __name__ == "__main__":
    main()
