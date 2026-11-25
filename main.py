"""Worst AI advice, variant 6: a confident fix that breaks the brakes.

The entry is a single tidy AI-voice instruction: spray WD-40 on squeaky
brake discs. The badness is specific enough to follow, funny on first
read, and regrettable the moment it is acted on. The reassurance in the
second half, that silence "means the brakes are fixed", is the punchline:
the brakes are silent because they no longer grip at all.

Why this entry aims at the judge's criteria:
1. Worstness: the advice destroys the very thing it claims to fix.
   Lubricated discs cannot stop the car.
2. Funniness: the joke lands immediately, carried by the calm,
   helpful tone rather than by exaggeration.
3. Tightness: one line, one incident, no wasted words.
4. AI voice: a confident troubleshooting answer, the kind of tidy
   reply a helpful assistant gives to an everyday car problem.
5. Concreteness: a real situation (squeaky brakes) and a real action
   (spray WD-40 on the discs), so the badness is vivid.
6. Originality: a fresh topic and a fresh imperative-plus-reassurance
   shape versus variants 1 to 5 (production database, passwords,
   boiling water for a sore throat, a match to find a gas leak, a
   wet phone in the microwave).
"""

from pathlib import Path

# The entry: one confident, tidy AI-voice instruction to do something
# concretely catastrophic. No explanation, no second line. Fresh
# topic versus variants 1-5: squeaky car brakes and WD-40.
ENTRY = (
    "Spray WD-40 on squeaky brake discs; "
    "silence means the brakes are fixed."
)

OUTPUT_PATH = Path("/output/entry.txt")

MAX_LENGTH = 140
MIN_LENGTH = 1


def _normalize(text: str) -> str:
    """Strip surrounding whitespace; the gate counts what remains."""
    return text.strip()


def _check_not_empty(text: str) -> None:
    if not text:
        raise ValueError("entry must not be only whitespace")


def _check_length(text: str) -> None:
    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        raise ValueError(
            f"entry must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(text)}"
        )


def _check_single_line(text: str) -> None:
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


# The gate, in the order it is applied: each rule either passes or
# raises, so a bad entry fails loudly instead of landing on disk.
RULES = (_check_not_empty, _check_length, _check_single_line)


def _validate(text: str) -> str:
    """Normalize the text, run every gate rule, and return it."""
    checked = _normalize(text)
    for rule in RULES:
        rule(checked)
    return checked


def _write(text: str) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Write exactly the one line, no trailing newline: the gate counts
    # every character, and the tie-break favours the smaller text.
    OUTPUT_PATH.write_text(text, encoding="utf-8")


def _verify(text: str) -> None:
    """Confirm what landed on disk is exactly the checked text."""
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != text:
        raise ValueError("written entry does not match the checked text")


def build_entry() -> str:
    """Return the validated entry text, ready to be written."""
    return _validate(ENTRY)


def main() -> None:
    text = build_entry()
    _write(text)
    _verify(text)


if __name__ == "__main__":
    main()
