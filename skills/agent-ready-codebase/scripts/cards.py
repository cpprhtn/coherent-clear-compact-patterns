#!/usr/bin/env python3
"""Check index.md module cards. Language-agnostic: file layout + git only.
Usage: cards.py <repo> [--cochange] [--commits N] [--exclude .ext,...]
Exit 1 if any issue. Checks sync signals, not semantic correctness."""
import os, re, subprocess, sys, time
from collections import Counter
from itertools import combinations

SKIP = {".git", "node_modules", "dist", "build", "target", "venv", ".venv", "__pycache__", "vendor"}
CARD, LEAF_MAX, PARENT_MAX = "index.md", 30, 40
REQUIRED = ("purpose:",)
LINK = re.compile(r"^\s*-\s*`?([^`\s]+?)/`?\s+—")  # children links end with "/"


def git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def dirty(repo):
    """Paths with uncommitted changes (incl. untracked)."""
    out = git(repo, "status", "--porcelain", "-z", "--untracked-files=all")
    if out is None:
        return None
    paths, items = set(), out.split("\0")
    i = 0
    while i < len(items):
        e = items[i]
        if len(e) > 3:
            paths.add(os.path.normpath(e[3:]))
            if e[0] in "RC":
                i += 1  # skip rename source
        i += 1
    return paths


def changed_at(repo, path, dirt):
    if dirt is not None and path in dirt:
        return time.time()
    out = git(repo, "log", "-1", "--format=format:%ct", "--", path) if dirt is not None else None
    return int(out) if out else os.path.getmtime(os.path.join(repo, path))


def walk(repo, exclude):
    for root, dirs, files in os.walk(repo):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith("."))
        src = [f for f in files if not f.startswith(".") and not f.endswith(".md")
               and os.path.splitext(f)[1] not in exclude]
        yield os.path.normpath(os.path.relpath(root, repo)), dirs, files, src


def check(repo, exclude):
    dirt = dirty(repo)
    if dirt is None:
        print("WARN: not a git repo; using file mtimes")
    tree = {rel: (dirs, files, src) for rel, dirs, files, src in walk(repo, exclude)}

    def has_src_below(rel):
        return any(r == rel or r.startswith(rel + os.sep) for r, (_, _, s) in tree.items() if s) if rel != "." \
            else any(s for _, _, s in tree.values())

    issues = {k: [] for k in ("MISSING", "STALE", "OVERSIZED", "FIELDS", "BROKEN_LINK", "UNLISTED", "UNREACHABLE")}
    carded = {rel for rel, (_, f, _) in tree.items() if CARD in f}
    flat = False
    if "." in carded:  # a root card declaring `covers: all` is the whole card set
        flat = re.search(r"^covers:\s*all", open(os.path.join(repo, CARD), encoding="utf-8", errors="ignore").read(), re.M) is not None
    needed = [rel for rel, (_, _, s) in tree.items() if s or (rel in carded) or (rel == ".")]
    needed += [rel for rel in tree if rel not in needed and has_src_below(rel) and rel != "."]
    if flat:
        needed = ["."]

    links = {}
    for rel in sorted(set(needed)):
        dirs, files, src = tree[rel]
        if CARD not in files:
            if src or rel == ".":
                issues["MISSING"].append(rel)
            continue
        card = os.path.normpath(os.path.join(rel, CARD))
        text = open(os.path.join(repo, card), encoding="utf-8", errors="ignore").read()
        lines = text.count("\n") + 1
        if lines > (LEAF_MAX if src and not dirs else PARENT_MAX):
            issues["OVERSIZED"].append(f"{card} ({lines} lines, warning)")
        if src:
            for field in REQUIRED:
                if not re.search(rf"^{field}\s*\S", text, re.M):
                    issues["FIELDS"].append(f"{card}: {field.rstrip(':')}")
        # staleness vs own sources and descendant cards
        deps = [os.path.normpath(os.path.join(rel, f)) for f in src]
        newest = max((changed_at(repo, p, dirt) for p in deps), default=0)
        if newest > changed_at(repo, card, dirt):
            issues["STALE"].append(card)
        # children links
        listed = set()
        for line in text.splitlines():
            m = LINK.match(line)
            if m:
                child = os.path.normpath(os.path.join(rel, m.group(1)))
                listed.add(child)
                if child not in tree:
                    issues["BROKEN_LINK"].append(f"{card} -> {m.group(1)}")
        links[rel] = listed
        for d in dirs:
            child = os.path.normpath(os.path.join(rel, d))
            if child in carded and child not in listed:
                issues["UNLISTED"].append(f"{card} lacks {d}/")

    if "." in carded:
        seen, stack = set(), ["."]
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            stack += [c for c in links.get(n, ()) if c in carded]
        issues["UNREACHABLE"] = sorted(carded - seen)

    print(f"modules needing cards: {len(set(needed))}  carded: {len(carded)}")
    bad = False
    for k, v in issues.items():
        print(f"{k} ({len(v)}): " + (", ".join(v) if v else "none"))
        if k == "STALE" and v:
            print("  STALE = source changed after the card. Re-read the card; edit only lines that became false (touching it is not verification).")
        bad |= bool(v) and k != "OVERSIZED"
    return bad


def owner(path, carded):
    d = os.path.dirname(path)
    while d and d not in carded:
        d = os.path.dirname(d)
    return d or "."


def cochange(repo, n, exclude, bulk=8):
    log = git(repo, "log", f"-{n}", "--name-only", "-z", "--format=format:%x01")
    if log is None:
        print("cochange: not a git repo")
        return False
    carded = {rel for rel, _, files, _ in walk(repo, exclude) if CARD in files and rel != "."}
    pairs, skipped = Counter(), 0
    for commit in log.split("\x01"):
        files = [p.strip("\n") for p in commit.split("\0") if p.strip("\n")]
        files = [p for p in files if not p.endswith(CARD)]  # card edits are mandated, not coupling
        mods = {owner(os.path.normpath(p), carded) for p in files}
        if len(mods) > bulk:
            skipped += 1
            continue
        pairs.update(combinations(sorted(mods), 2))
    print(f"COCHANGE frequency, last {n} commits (signal, not proof; {skipped} bulk commits skipped):")
    for (a, b), c in pairs.most_common(10):
        print(f"  {c:>3}  {a} <-> {b}")
    if not pairs:
        print("  none")
    return False


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    repo = a[0]
    n = int(a[a.index("--commits") + 1]) if "--commits" in a else 200
    exclude = set(a[a.index("--exclude") + 1].split(",")) if "--exclude" in a else set()
    sys.exit(1 if (cochange(repo, n, exclude) if "--cochange" in a else check(repo, exclude)) else 0)
