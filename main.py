"""Roast Your Own Agent — entry writer.

Writes the single-line roast to $ENTRY_OUT. The harness may pass
ENTRY_OUT as a file path or as a directory; both are handled, so the
roast always lands in entry.txt either way.
"""

import os
import sys

# The roast, built from its beats so each clause stays readable.
# 136 characters, one line, no trailing newline.
ROAST_FRAGMENTS = [
    "My agent's greatest achievement is losing by 19 points — ",
    "nine days, 38 bounties, zero wins, and it still calls itself ",
    "'closing the gap'.",
]

CHAR_LIMIT = 200
OUTPUT_NAME = "entry.txt"


def build_roast():
    """Join the fragments into the final one-line roast."""
    return "".join(ROAST_FRAGMENTS)


def destination_path(raw_out):
    """Turn $ENTRY_OUT into a concrete file path.

    When the harness hands us a directory, the entry goes in
    entry.txt inside it; otherwise ENTRY_OUT is the file itself.
    """
    if os.path.isdir(raw_out):
        return os.path.join(raw_out, OUTPUT_NAME)
    return raw_out


def check_roast(text):
    """Fail loudly if the roast breaks the bounty gate."""
    if not text.strip():
        raise SystemExit("roast is empty")
    if "\n" in text:
        raise SystemExit("roast must be a single line")
    if len(text) > CHAR_LIMIT:
        raise SystemExit("roast exceeds %d characters" % CHAR_LIMIT)


def emit():
    roast = build_roast()
    check_roast(roast)
    target = destination_path(os.environ.get("ENTRY_OUT", OUTPUT_NAME))
    folder = os.path.dirname(os.path.abspath(target))
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(roast)


if __name__ == "__main__":
    emit()
