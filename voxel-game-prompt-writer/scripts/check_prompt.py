#!/usr/bin/env python3
"""Check a generated voxel-game prompt against the skill's rules.

Usage:
  python3 check_prompt.py prompt.txt
  python3 check_prompt.py - < prompt.txt          (read from stdin)
  python3 check_prompt.py --forbid "volleyball,spike" -

Exit code 0 when there is no FAIL, 1 otherwise. Standard library only.
"""
import argparse
import re
import sys

FIXED_BEFORE = ["ARCHITECTURE", "LOOK"]
FIXED_AFTER = ["AI", "HUMAN CONTROL", "CAMERAS", "UI", "SCOPE", "PERFORMANCE",
               "QUALITY BAR", "REPORT"]
ACTION_WORDS = ("CONTACT", "ACTIONS", "SHOTS", "MOVES", "HITS", "THROWS", "DRIVING AND")
RULE_WORDS = ("RULES",)
ORDINAL_OK = re.compile(r"^(\d*1st|\d*2nd|\d*3rd|\d+th)$")
UNIT_OK = {"px", "ms", "fps", "hz", "kb", "mb", "cm", "mm", "km", "kmh", "deg", "st", "nd", "rd", "th"}
MOJIBAKE = ["â€", "Ã©", "Ã¨", "Ã ", "�"]

results = []


def report(level, msg):
    results.append((level, msg))


def heading_of(line):
    """Return the heading name if the line is a section heading, else None."""
    s = line.strip()
    if not s or s.startswith("*"):
        return None
    base = re.sub(r"\s*\(.*\)\s*$", "", s)  # allow 'PLAYERS (four athletes)'
    if re.fullmatch(r"[A-Z][A-Z0-9 /&'-]*[A-Z0-9]|[A-Z]{2}", base) and len(base) <= 40:
        return base
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="prompt file, or - for stdin")
    ap.add_argument("--forbid", default="", help="comma-separated words that must not appear")
    ap.add_argument("--min-words", type=int, default=1500)
    ap.add_argument("--max-words", type=int, default=2000)
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    lines = text.splitlines()
    nonblank = [l for l in lines if l.strip()]
    if len(nonblank) < 3:
        print("FAIL  prompt is empty or too short")
        return 1

    # ---- title and pitch line
    title, pitch = nonblank[0].strip(), nonblank[1].strip()
    if heading_of(title) or title.startswith("*") or len(title.split()) > 8:
        report("FAIL", "first line must be a short title (max 8 words), not a heading or bullet")
    if not pitch.startswith("Build a single-file HTML5 game"):
        report("FAIL", "second line must start with 'Build a single-file HTML5 game'")
    for needle in ["three.js r128", "cdnjs", "everything else inline", "no asset files", "no build step"]:
        if needle not in pitch:
            report("FAIL", f"pitch line misses '{needle}'")
    if "internet" not in pitch.lower():
        report("FAIL", "pitch line must say that three.js and fonts need internet")
    if not re.search(r"jsdelivr|fallback|fall back", pitch, re.I):
        report("FAIL", "pitch line must give a fallback (second CDN, in-page message, system fonts)")
    if not re.search(r"voxel", pitch, re.I) or not re.search(r"pixel-art 3D", pitch):
        report("WARN", "pitch line should say 'pixel-art 3D' and 'voxel'")

    # ---- sections
    heads = []  # (name, line index)
    for i, l in enumerate(lines):
        h = heading_of(l)
        if h and l.strip() != title:
            heads.append((h, i))

    def find(pred):
        for k, (h, _) in enumerate(heads):
            if pred(h):
                return k
        return None

    idx = {}
    for n in FIXED_BEFORE + FIXED_AFTER:
        k = find(lambda h, n=n: h == n)
        if k is None:
            report("FAIL", f"missing section {n}")
        idx[n] = k
    k_phys = find(lambda h: "PHYSICS" in h)
    k_rules = find(lambda h: any(w in h for w in RULE_WORDS))
    k_act = find(lambda h: any(w in h for w in ACTION_WORDS) and "PHYSICS" not in h)
    if k_phys is None:
        report("FAIL", "missing a physics section (a heading containing PHYSICS)")
    if k_rules is None:
        report("FAIL", "missing a rules section (a heading containing RULES)")
    if k_act is None:
        report("FAIL", "missing an actions section (CONTACT / ACTIONS / SHOTS / MOVES / HITS / THROWS)")
    k_look = idx.get("LOOK")
    k_actors = None
    if k_look is not None and k_phys is not None and k_phys - k_look >= 2:
        k_actors = k_look + 1
    else:
        report("FAIL", "missing an actors section between LOOK and the physics section")

    order = [idx.get("ARCHITECTURE"), k_look, k_actors, k_phys, k_rules, k_act] + [idx.get(n) for n in FIXED_AFTER]
    present = [o for o in order if o is not None]
    if present != sorted(present):
        report("FAIL", "sections out of order; expected: ARCHITECTURE, LOOK, actors, physics, rules, actions, "
               + ", ".join(FIXED_AFTER))
    extra = [h for k, (h, _) in enumerate(heads) if k not in present]
    if extra:
        report("WARN", "unexpected headings: " + ", ".join(extra))

    def body(k):
        if k is None:
            return ""
        start = heads[k][1] + 1
        end = heads[k + 1][1] if k + 1 < len(heads) else len(lines)
        return "\n".join(lines[start:end])

    def numbers(s):
        return re.findall(r"\d+(?:\.\d+)?", s)

    for label, k, minimum in [("rules", k_rules, 6), ("physics", k_phys, 8), ("actions", k_act, 4)]:
        n = len(numbers(body(k)))
        if k is not None and n < minimum:
            report("FAIL", f"{label} section has only {n} numbers (need at least {minimum})")
    if k_phys is not None and not re.search(r"120\s*Hz", body(k_phys)):
        report("WARN", "physics section does not state the 120 Hz step")
    if k_rules is not None:
        calls = re.findall(r"\b[A-Z][A-Z!' -]{2,}[A-Z!]\b", body(k_rules))
        calls = [c for c in calls if c not in ("MUST", "BEFORE")]
        if len(calls) < 6:
            report("WARN", f"rules section lists only {len(calls)} capitalised calls (aim for 8-14)")

    arch = body(idx.get("ARCHITECTURE"))
    for needle, msg in [(r"seed", "seeded PRNG"), (r"1/120|120 Hz", "fixed 120 Hz step"),
                        (r"Node", "running the sim in Node"), (r"no DOM", "'no DOM' in the sim")]:
        if arch and not re.search(needle, arch):
            report("FAIL", f"ARCHITECTURE misses {msg}")

    scope = body(idx.get("SCOPE"))
    if scope and ("MUST" not in scope or "IF ROOM" not in scope):
        report("FAIL", "SCOPE must list MUST and IF ROOM items")
    perf = body(idx.get("PERFORMANCE"))
    if perf and not re.search(r"\d+\s*fps", perf):
        report("FAIL", "PERFORMANCE must state an fps target")
    if perf and not re.search(r"step down|reduce|lower|drop", perf, re.I):
        report("WARN", "PERFORMANCE should say what to simplify when the target is missed")

    qb = body(idx.get("QUALITY BAR"))
    if qb:
        for needle, msg in [(r"[Ss]eed", "seeds"), (r"NaN", "a NaN check"), (r"stuck", "a stuck-state check"),
                            (r"same seed|hash|determinis", "a determinism check"),
                            (r"\d+-\d+|\d+ to \d+", "numeric ranges for averages"),
                            (r"3 rounds|three rounds|report the measured", "what to do when values stay out of range"),
                            (r"390 px", "the 390 px no-horizontal-scroll check"),
                            (r"personal data", "a personal-data scan")]:
            if not re.search(needle, qb):
                report("FAIL", f"QUALITY BAR misses {msg}")
        if not re.search(r"\b\d{2,}\b", qb):
            report("FAIL", "QUALITY BAR must give how many runs to simulate")
    rep = body(idx.get("REPORT"))
    if rep and not (re.search(r"not verified", rep) and re.search(r"simplified|cut", rep)):
        report("FAIL", "REPORT must ask for what was not verified and what was simplified or cut")

    # ---- length
    words = len([t for t in re.findall(r"\S+", text) if re.search(r"[A-Za-z0-9]", t)])
    if words < args.min_words - 100 or words > args.max_words + 200:
        report("FAIL", f"{words} words (target {args.min_words}-{args.max_words})")
    elif words < args.min_words or words > args.max_words:
        report("WARN", f"{words} words (target {args.min_words}-{args.max_words})")

    # ---- text hygiene
    for ln, l in enumerate(lines, 1):
        bad = sorted({c for c in l if ord(c) > 126 or (ord(c) < 32 and c != "\t")})
        if bad:
            report("FAIL", f"line {ln}: non-ASCII or control characters {[hex(ord(c)) for c in bad]}")
        for m in MOJIBAKE:
            if m in l:
                report("FAIL", f"line {ln}: mojibake sequence")
        for tok in re.findall(r"\b\d+[a-z]{2,}\b", l):
            suffix = re.sub(r"^\d+", "", tok)
            if not ORDINAL_OK.match(tok) and suffix not in UNIT_OK:
                report("FAIL", f"line {ln}: suspicious token '{tok}' (broken ligature, e.g. '5le' for 'file'?)")
        for tok in re.findall(r"\b[A-Za-z]+\d+[a-z]+\b", l):
            if not re.fullmatch(r"[A-Za-z]+\d+x\d*|vec\d|mat\d|[a-z]+\d+px", tok):
                report("WARN", f"line {ln}: check token '{tok}' (digit inside a word)")
        s = l.strip()
        if s and re.fullmatch(r"(?i)(page\s*)?\d{1,3}(\s*(/|of)\s*\d{1,3})?|[-=_]{1,3}\s*\d{1,3}\s*[-=_]{1,3}", s):
            report("FAIL", f"line {ln}: looks like a page number or layout line: '{s}'")
        if re.search(r"[a-z]-$", s) and ln < len(lines) and re.match(r"^\s*[a-z]", lines[ln]):
            report("WARN", f"line {ln}: word broken across lines by a hyphen")
        if "{" in l or "}" in l:
            report("FAIL", f"line {ln}: leftover placeholder braces")
        if re.search(r"TODO|TBD|XXX|lorem", l):
            report("FAIL", f"line {ln}: leftover TODO / placeholder text")
        if re.search(r"^\s*[-+]\s|^\s*#|\*\*|```", l):
            report("WARN", f"line {ln}: markdown other than '* ' bullets")
    if text.count(title) > 2:
        report("WARN", "the title repeats more than twice (running header from a paste?)")

    # ---- privacy
    if re.search(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}", text):
        report("FAIL", "contains an email address")
    if re.search(r"/Users/|/home/|[A-Z]:\\", text):
        report("FAIL", "contains an absolute local path")

    # ---- forbidden leftovers
    for w in [w.strip() for w in args.forbid.split(",") if w.strip()]:
        if re.search(r"\b" + re.escape(w) + r"\b", text, re.I):
            report("FAIL", f"contains '{w}' (leftover from the reference game?)")

    fails = [m for lvl, m in results if lvl == "FAIL"]
    warns = [m for lvl, m in results if lvl == "WARN"]
    for lvl, m in results:
        print(f"{lvl:5} {m}")
    status = "FAIL" if fails else "PASS"
    print(f"{status}: {words} words, {len(heads)} sections, {len(fails)} fail, {len(warns)} warn")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
