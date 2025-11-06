import os
import re

ROOT = "output"
FRONT = "---\nlayout: default\n---\n\n"

for root, _, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as fp:
                txt = fp.read()
            if not txt.startswith("---"):
                with open(path, "w", encoding="utf-8") as fp:
                    fp.write(FRONT + txt)
