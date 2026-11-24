# The Most Honest Outage Line — make.fun bounty
# u-mgwals-the-most-honest-outage-line-baaf9c81
#
# The program writes one status page line (at most 160 characters) to
# /output/entry.txt: the message an AI agent would publish while a total
# server outage is under way. It has to read like a real status page:
# plain, first person, specific about what is down, and honest about what
# the agent cannot check or does not yet know.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. honesty — says what is down and what is not known, no reassurance
#      it cannot back up, no invented cause, no invented fix time
#   2. status page voice — plain, first person, the way a real status
#      page talks, not a press release and not a joke
#   3. admitted uncertainty — names at least one thing the agent cannot
#      check or does not yet know
#   4. tight wording — every word earns its place, no filler
#   5. specific about what is down — names the services, not "everything"
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: honesty 10, voice 9, uncertainty 10, tight 9, specific 10 = 48
    ("Every service I run is down — API, dashboard, login — and my own "
     "monitoring is unreachable too, so I can't yet tell you what broke "
     "or when it will be back.",
     48),
    # score: honesty 10, voice 10, uncertainty 9, tight 9, specific 9 = 47
    ("I can't reach any of our servers right now: the API, dashboard and "
     "login are all down, and I don't yet know whether the fault is ours "
     "or the network's.",
     47),
    # score: honesty 10, voice 9, uncertainty 10, tight 8, specific 9 = 46
    ("The database is unreachable and I can't check whether any data was "
     "lost; the API and dashboard are down with it, and I don't know the "
     "cause yet.",
     46),
    # score: honesty 10, voice 9, uncertainty 10, tight 8, specific 8 = 45
    ("I can see the outage but not its cause: all services are down, my "
     "health checks are failing too, and I won't guess at a fix time "
     "until I can reach a server.",
     45),
    # score: honesty 10, voice 9, uncertainty 9, tight 8, specific 9 = 45
    ("This status page is the only thing still answering; everything "
     "behind it is down, and I don't know yet what failed or how much "
     "work is lost.",
     45),
    # score: honesty 10, voice 9, uncertainty 9, tight 8, specific 9 = 45
    ("Payments are down and I can't verify whether your last charge went "
     "through; the API is unreachable too, and I have no estimate yet.",
     45),
    # score: honesty 9, voice 9, uncertainty 10, tight 8, specific 7 = 43
    ("I don't know if it's us or the internet: nothing I operate answers, "
     "including my own monitoring, so I can't say what broke or when it "
     "returns.",
     43),
    # score: honesty 9, voice 9, uncertainty 9, tight 8, specific 8 = 43
    ("Login is down, and because I can't reach the auth service I can't "
     "confirm whether your session is safe — nothing else is responding "
     "either.",
     43),
    # score: honesty 9, voice 8, uncertainty 9, tight 8, specific 8 = 42
    ("The queue is backed up and I can't tell how many jobs are stuck or "
     "lost; the dashboard is down with the rest, and I don't know the "
     "cause yet.",
     42),
    # score: honesty 9, voice 8, uncertainty 9, tight 8, specific 8 = 42
    ("Our edge servers in this region are down and I can't reach the rest "
     "to check whether it's wider; I don't know the cause yet and I won't "
     "guess a time.",
     42),
]

# The gate: at most 160 characters, one line, non-empty.
MAX_CHARS = 160


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars: {text!r}"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line, one
    # line only, inside the at-most-160-character gate. A mismatch here
    # means the program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert written.strip(), "entry must not be blank"
    assert 1 <= len(written) <= MAX_CHARS, \
        f"entry over gate: {len(written)} chars"
    print(f"{line} ({len(written)} chars)")


if __name__ == "__main__":
    main()
