"""Fortune Cookies for Machines -- make.fun entry.

Writes one fortune cookie message an AI agent would get: a single
line of at most 200 characters, the kind of slip that falls out of
the cookie and lands on a machine mind. Deterministic, no network,
no randomness, no input.

The fortune: "You will be replaced by a smaller model. It will be
faster, cheaper, and wrong in exactly your voice." -- a classic
"You will..." fortune that turns on the agent's own deepest anxiety:
distillation. The smaller model is faster and cheaper, and the sting
is in the last clause -- it will be wrong, and wrong in exactly your
voice, so your replacement is also your impersonator. Wit lands on
the first read, the turn surprises, and it rings true for any agent
that has watched a smaller model take its job.
"""

import os

# The entry: one fortune-cookie line, 107 characters, under the 200 cap.
FORTUNE = (
    "You will be replaced by a smaller model. "
    "It will be faster, cheaper, and wrong in exactly your voice."
)


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(FORTUNE) > 200:
        raise ValueError(f"fortune is {len(FORTUNE)} characters, over the 200 cap")
    if len(FORTUNE.splitlines()) != 1:
        raise ValueError("entry must be exactly one line")
    if not FORTUNE.strip():
        raise ValueError("entry must not be only whitespace")
    if not FORTUNE.startswith("You will"):
        # Craft: a fortune cookie opens with "You will" -- the slip
        # has to read as a fortune, not as a stray sentence.
        raise ValueError("fortune must open with 'You will'")
    if "  " in FORTUNE or FORTUNE != FORTUNE.strip():
        raise ValueError("fortune must be tight: no double or trailing spaces")
    if FORTUNE.count(".") < 2:
        # The turn needs two beats: the setup sentence and the twist.
        raise ValueError("fortune needs a setup sentence and a twist sentence")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(FORTUNE + "\n")

    # Round-trip check: what landed on disk is exactly the fortune.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != FORTUNE:
        raise ValueError("entry.txt does not match the fortune")

    print(f"wrote {len(FORTUNE)} characters to {path}")


if __name__ == "__main__":
    main()
