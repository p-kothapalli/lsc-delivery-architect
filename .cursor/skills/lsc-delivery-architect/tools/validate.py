#!/usr/bin/env python3
"""
LSC Delivery Architect — parity and artifact validator.

Three independent groups of checks:

  PAYLOAD   the skill is internally consistent (no orphan or dangling
            references, claimed counts match reality, every authorised badge
            has a style, Pattern F exists)
  DOCS      the published guide matches the payload it ships alongside
            (version stamp, reference count, object count, no stale phrases)
  ARTIFACT  a generated story or prototype satisfies the blockers that can be
            checked deterministically

The split matters: PAYLOAD and DOCS are the drift this repo has actually
suffered — a two-version divergence that nothing detected for a month. ARTIFACT
is the RULE-13 / Pattern-E / self-check class, where prose enforcement measured
near-zero compliance and structure measured near-zero violations.

Stdlib only, no network. Exit 1 on any FAIL, or on WARN under --strict.

    ./validate.py                                  # payload + docs if present
    ./validate.py --artifacts requirements/*.md    # add artifact linting
    ./validate.py --json                           # machine-readable
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field

FAIL, WARN, INFO = "FAIL", "WARN", "INFO"
STALE_AFTER_DAYS = 180


@dataclass
class Finding:
    level: str
    code: str
    message: str
    where: str = ""


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, level: str, code: str, message: str, where: str = "") -> None:
        self.findings.append(Finding(level, code, message, where))

    def ok(self, code: str, message: str) -> None:
        self.add(INFO, code, message)

    def counts(self) -> dict[str, int]:
        return {lv: sum(1 for f in self.findings if f.level == lv) for lv in (FAIL, WARN, INFO)}


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- payload ----

def strip_version_history(skill_text: str) -> str:
    """Changelog rows record what past versions claimed and are immutable.

    v1.4's row legitimately says the catalog held "~350" objects, because that
    is what v1.4 asserted. Counting it as a live claim would make the check
    permanently unfixable.
    """
    marker = re.search(r"^#+\s*Version [Hh]istory", skill_text, re.M)
    return skill_text[: marker.start()] if marker else skill_text


def catalog_object_count(catalog: pathlib.Path) -> int:
    return len(re.findall(r"^\|\s*\*\*[A-Za-z][A-Za-z0-9_]*\*\*\s*\|", read(catalog), re.M))


def check_payload(skill_dir: pathlib.Path, rep: Report) -> dict:
    facts: dict = {}
    skill_md = skill_dir / "SKILL.md"
    refs_dir = skill_dir / "references"

    if not skill_md.is_file():
        rep.add(FAIL, "P01", "SKILL.md not found", str(skill_md))
        return facts
    skill_text = read(skill_md)

    m = re.search(r"^#\s*LSC Delivery Architect\s*\(v([\d.]+)\)", skill_text, re.M)
    if not m:
        rep.add(FAIL, "P01", "cannot parse the version from SKILL.md's H1")
    else:
        facts["version"] = m.group(1)
        rep.ok("P01", f"skill version v{m.group(1)}")

    # --- reference wiring: both directions ---
    on_disk = {p.name for p in sorted(refs_dir.glob("*.md"))} if refs_dir.is_dir() else set()
    facts["reference_count"] = len(on_disk)
    cited = set(re.findall(r"references/([a-z0-9._-]+\.md)", skill_text))

    for orphan in sorted(on_disk - cited):
        rep.add(WARN, "P02", f"reference exists but SKILL.md never cites it — unreachable", f"references/{orphan}")
    for dangling in sorted(cited - on_disk):
        rep.add(FAIL, "P03", "SKILL.md cites a reference that does not exist", f"references/{dangling}")
    if on_disk and not (on_disk - cited) and not (cited - on_disk):
        rep.ok("P02", f"all {len(on_disk)} references cited and present")

    # Rule-file citations, the class that produced a dead pointer in v1.10.
    for mdc in sorted(set(re.findall(r"([a-z0-9-]+\.mdc)", skill_text))):
        roots = [skill_dir.parent.parent / "rules" / mdc, skill_dir.parent.parent.parent / ".cursor" / "rules" / mdc]
        if not any(r.is_file() for r in roots):
            rep.add(WARN, "P03", f"SKILL.md cites a rule file that is not in .cursor/rules/", mdc)

    # --- claimed object counts vs the catalog itself ---
    catalog = refs_dir / "lsc-standard-objects-catalog.md"
    if catalog.is_file():
        actual = catalog_object_count(catalog)
        facts["object_count"] = actual
        rep.ok("P04", f"catalog holds {actual} objects")
        for src in [skill_md] + sorted(refs_dir.glob("*.md")):
            body = strip_version_history(read(src)) if src.name == "SKILL.md" else read(src)
            for claim in re.finditer(r"(~?\d{3})\+?\s+(?:catalogued\s+)?(?:LSC\s+)?(?:standard\s+)?objects?\b", body):
                raw = claim.group(1)
                if raw.lstrip("~") != str(actual):
                    line = body[: claim.start()].count("\n") + 1
                    rep.add(FAIL, "P04", f"claims {raw} objects; the catalog holds {actual}",
                            f"{src.name}:{line}")
    else:
        rep.add(WARN, "P04", "object catalog reference missing — count parity not checked")

    # --- AC patterns ---
    acs = refs_dir / "ac-pattern-library.md"
    if acs.is_file():
        letters = sorted(set(re.findall(r"^#+\s*Pattern ([A-Z])\b", read(acs), re.M)))
        facts["ac_patterns"] = letters
        rep.ok("P05", f"AC patterns defined: {'–'.join([letters[0], letters[-1]]) if letters else 'none'}")
        if "F" not in letters:
            rep.add(FAIL, "P05", "Pattern F (offline/sync) is not defined, but RULE 16 makes it "
                                 "mandatory whenever Surface includes offline iPad")
        expected = [chr(c) for c in range(ord("A"), ord(letters[-1]) + 1)] if letters else []
        for gap in [c for c in expected if c not in letters]:
            rep.add(WARN, "P05", f"Pattern {gap} is referenced by the A–{letters[-1]} range but not defined")

    # --- badge vocabulary: authorised vs styled ---
    primer = refs_dir / "slds2-lsc-primer.md"
    if primer.is_file():
        styled = set(re.findall(r"\.lsc-badge\.([a-z0-9]+)", read(primer)))
        facts["badges_styled"] = sorted(styled)
        authorised: set[str] = set()
        for name in ("plan-prototype-mode.md", "post-generation-offers.md"):
            p = refs_dir / name
            if not p.is_file():
                continue
            body = read(p)
            authorised |= {b.lower() for b in re.findall(r"\blsc-badge\s+([a-z0-9]+)\b", body)}
            # The authoritative list is prose: "**Badges** — one of: `OOTB`, `Config`, …"
            for line in re.findall(r"^.*\bBadges?\b.*?one of:(.*)$", body, re.M):
                authorised |= {t.lower() for t in re.findall(r"`([A-Za-z]{2,6})`", line)}
        unstyled = authorised - styled
        for b in sorted(unstyled):
            rep.add(FAIL, "P06", f"badge '{b}' is authorised for prototypes but has no style in the primer — "
                                 f"it renders unlabelled", "slds2-lsc-primer.md")
        if not unstyled:
            rep.ok("P06", f"{len(styled)} badge styles cover every authorised badge")

    # --- decaying verification claims ---
    today = dt.date.today()
    dated = 0
    for src in [skill_md] + sorted(refs_dir.glob("*.md")):
        body = strip_version_history(read(src)) if src.name == "SKILL.md" else read(src)
        for vm in re.finditer(r"[Vv]erified[^.\n]{0,80}?(\d{4}-\d{2}-\d{2})", body):
            dated += 1
            try:
                age = (today - dt.date.fromisoformat(vm.group(1))).days
            except ValueError:
                continue
            if age > STALE_AFTER_DAYS:
                line = body[: vm.start()].count("\n") + 1
                rep.add(WARN, "P07", f"verification is {age} days old — re-check against current docs",
                        f"{src.name}:{line}")
    facts["dated_verifications"] = dated
    rep.ok("P07", f"{dated} dated verification note(s) across the payload")
    if dated < 5:
        rep.add(WARN, "P07", f"only {dated} platform claim(s) carry a verification date, so there is no way "
                             f"to tell what the per-release review needs to re-check")
    return facts


# ------------------------------------------------------------------- docs ----

NUM_WORDS = {n: w for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen".split())}

STALE_PHRASES = [
    (r"Patterns? A[–\-]E\b", "names the AC patterns as A–E; Pattern F exists"),
    (r"if it starts writing before ask", "states question-first absolutely; RULE 2 now sanctions a labelled DRAFT"),
    (r"source of truth for whether the skill", "oversells the evaluations as full coverage"),
    (r"curated catalog reference and flags", "sends the reader to the dated catalog as a fallback authority"),
]


def check_docs(docs: pathlib.Path, facts: dict, rep: Report) -> None:
    html = read(docs)

    version = facts.get("version")
    stamps = re.findall(r"Skill v([\d.]+)", html)
    if version and stamps:
        for s in set(stamps):
            if s != version:
                rep.add(FAIL, "D01", f"guide stamps v{s} but the payload beside it is v{version}", docs.name)
        if set(stamps) == {version}:
            rep.ok("D01", f"guide version stamp matches the payload (v{version})")
    elif version:
        rep.add(WARN, "D01", "guide carries no 'Skill vX.Y' stamp, so drift is invisible to a reader", docs.name)

    n = facts.get("reference_count")
    if n:
        word = NUM_WORDS.get(n, str(n))
        for m in re.finditer(r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                             r"thirteen|fourteen|fifteen|sixteen|\d{1,2})\s+references\b", html, re.I):
            claim = m.group(1).lower()
            if claim not in (word, str(n)):
                rep.add(FAIL, "D02", f"guide says '{m.group(0).strip()}' but the payload ships {n}", docs.name)
        rep.ok("D02", f"reference count parity checked against {n} on disk")

    actual = facts.get("object_count")
    if actual:
        for m in re.finditer(r"(~?\d{3})\+?\s+(?:catalogued\s+)?(?:LSC\s+)?(?:standard\s+)?objects?\b", html):
            if m.group(1).lstrip("~") != str(actual):
                rep.add(FAIL, "D03", f"guide claims {m.group(1)} objects; the catalog holds {actual}", docs.name)

    # Every shipped reference should be discoverable in the guide's file tree.
    refs = (docs.parent / ".cursor/skills/lsc-delivery-architect/references")
    if refs.is_dir():
        for p in sorted(refs.glob("*.md")):
            if p.name not in html:
                rep.add(WARN, "D04", f"reference is shipped but never named in the guide — a reader "
                                     f"cannot discover it", p.name)

    for pattern, why in STALE_PHRASES:
        if re.search(pattern, html, re.I):
            rep.add(WARN, "D05", f"stale phrasing: {why}", docs.name)


# --------------------------------------------------------------- artifacts ----

GENERIC_PERSONAS = [r"\bas an? (?:user|business user|developer|admin|system)\b"]

GWT_LINE = re.compile(r"^\s*(?:\*\*)?(Given|When|Then|And)(?:\*\*)?\b(.*)$", re.I)

IMPL_IN_AC = [
    (r"\b\w+__[cr]\b", "custom API name"),
    (r"\b[A-Z][A-Za-z0-9]*(?:Service|Controller|Handler|Helper|Batch|Trigger|Selector|Repository)\b", "Apex class name"),
    (r"\bSELECT\b.+\bFROM\b", "SOQL"),
    (r"\bStep\s*\d+\b", "OmniScript step number"),
    (r"\bpermission set\b", "permission-set reference"),
    (r"\bIntegration Procedure\b|\bDataRaptor\b|\bData Mapper\b", "OmniStudio component"),
]


def lint_story(path: pathlib.Path, rep: Report, catalog_names: set[str]) -> None:
    text = read(path)
    loc = path.name
    obsolete = re.search(r"obsolet|superseded|do not (?:reuse|use)", text[:4000], re.I)
    lv = WARN if obsolete else FAIL  # a banner-carrying artifact is already flagged as unfit

    # Plan mode writes "Primary persona:"; stories write "Persona:". Both satisfy
    # the persona contract, so the check keys on aliases rather than one spelling.
    HEADER_ALIASES = {
        "Persona": (["Persona", "Primary persona"], "the persona contract"),
        "Surface": (["Surface"], "RULE 16"),
        "Offline": (["Offline"], "RULE 16"),
    }
    headers = {}
    for key, (aliases, _) in HEADER_ALIASES.items():
        for alias in aliases:
            m = re.search(rf"^\*\*{alias}:?\*\*:?\s*(.+)$", text, re.M | re.I)
            if m:
                headers[key] = m.group(1).strip()
                break

    for key, (aliases, rule) in HEADER_ALIASES.items():
        if key not in headers:
            spelling = " / ".join(f"**{a}:**" for a in aliases)
            rep.add(lv, "A01", f"missing required header field {spelling} ({rule})", loc)

    for pat in GENERIC_PERSONAS:
        if re.search(pat, text, re.I):
            rep.add(lv, "A02", "generic persona — must be a concrete LSC business role", loc)
            break

    surface = headers.get("Surface", "")
    offline = headers.get("Offline", "")
    needs_f = "ipad" in surface.lower() and "offline" in (surface + " " + offline).lower() \
        and not re.search(r"not required|n-?a\b", offline, re.I)
    if needs_f and "Pattern F" not in text:
        rep.add(lv, "A04", f"Surface/Offline require offline behaviour but no Pattern F AC is present "
                           f"(Surface: {surface!r}, Offline: {offline!r})", loc)

    # Pattern E completeness: "etc." anywhere in a field spec defeats the point.
    for m in re.finditer(r"^\|.*\betc\.?\b.*\|$", text, re.M | re.I):
        rep.add(lv, "A03", f"'etc.' inside a field-spec table — Pattern E requires every field enumerated",
                f"{loc}:{text[: m.start()].count(chr(10)) + 1}")

    # RULE 13: implementation identifiers inside acceptance criteria.
    for i, line in enumerate(text.splitlines(), 1):
        m = GWT_LINE.match(line)
        if not m:
            continue
        body = m.group(2)
        for pat, label in IMPL_IN_AC:
            if re.search(pat, body):
                rep.add(lv, "A05", f"{label} inside a Given/When/Then line — belongs in Technical Implementation",
                        f"{loc}:{i}")
                break
        else:
            for name in catalog_names:
                if re.search(rf"\b{name}\b", body):
                    rep.add(lv, "A05", f"standard object API name '{name}' inside an acceptance criterion",
                            f"{loc}:{i}")
                    break

    if not re.search(r"Estimated Effort|Effort\s*\|", text, re.I):
        rep.add(lv, "A06", "no Estimated Effort table", loc)


def used_in_markup(markup: str, cls: str) -> bool:
    """True only if the class is applied to an element.

    Searching the raw file for a class name is not enough: it matches the CSS
    rule that defines it, and — worse — it matches a self-check comment saying
    the element is *missing*. Both produce a false pass.
    """
    return re.search(rf'class="[^"]*\b{re.escape(cls)}\b', markup) is not None


def lint_prototype(path: pathlib.Path, rep: Report) -> None:
    raw = read(path)
    loc = path.name

    # Whole-artifact retirement, not a passing mention of the word in a caveat
    # about one detail.
    retired = re.search(r"OBSOLETE|DO NOT REUSE|superseded by", raw[:6000])
    lv = WARN if retired else FAIL

    body = re.sub(r"<!--.*?-->", "", raw, flags=re.S)          # drop comments
    markup = re.sub(r"<(style|script)\b.*?</\1>", "", body, flags=re.S | re.I)

    head = raw[:4000]
    declared = re.search(r"passed:\s*(\d+)\s*/\s*(\d+)", head)
    surface = re.search(r"surface:\s*(.+)", head)
    surface_txt = (surface.group(1) if surface else "").lower()
    wants_ipad = "ipad" in surface_txt or "both" in surface_txt
    wants_offline = "offline" in surface_txt

    # The mechanically-checkable subset of the primer's 12-point check.
    mech = {
        1: (":root" in body and "--slds-g-" in body, "root token block (check 1)"),
        4: (not re.search(r"font-size:\s*\d+px", body), "no hardcoded font-size (check 4)"),
        8: (len(re.findall(r'class="[^"]*\blsc-badge\b', markup)) >= 3,
            "interactive elements carry badges (check 8)"),
        9: (used_in_markup(markup, "lsc-build-banner"), "build-technology banner (check 9)"),
        10: ("prefers-color-scheme" not in body, "no dark-mode overrides (check 10)"),
    }
    if wants_ipad:
        mech[11] = (used_in_markup(markup, "lsc-ipad-frame"), "iPad frame for an iPad surface (check 11)")
    if wants_offline:
        mech[12] = (re.search(r'class="[^"]*offline', markup) is not None
                    and re.search(r"pending", markup, re.I) is not None,
                    "offline state with a pending-sync pill (check 12)")

    failed = [f"#{k} {desc}" for k, (passed, desc) in sorted(mech.items()) if not passed]

    if not declared:
        rep.add(lv, "A10", "no 'passed: X / Y' self-check header — §6.7 requires the score be declared", loc)
    else:
        got, total = int(declared.group(1)), int(declared.group(2))
        if total not in (10, 12):
            rep.add(WARN, "A10", f"self-check denominator is {total}; the current primer defines 12 points", loc)
        if got == total and failed:
            rep.add(lv, "A10", f"self-check claims a clean {got}/{total} but {len(failed)} mechanical "
                               f"check(s) fail: {'; '.join(failed)}", loc)

    for desc in failed:
        rep.add(lv, "A11", f"prototype fails {desc}", loc)

    if not surface:
        rep.add(lv, "A12", "no 'surface:' declaration in the self-check header (RULE 16)", loc)


# ------------------------------------------------------------------- main ----

def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the LSC Delivery Architect payload, docs and artifacts.")
    here = pathlib.Path(__file__).resolve().parent.parent
    ap.add_argument("--skill", type=pathlib.Path, default=here, help="skill directory (default: this script's parent)")
    ap.add_argument("--docs", type=pathlib.Path, default=None, help="published guide (default: repo-root index.html)")
    ap.add_argument("--artifacts", type=pathlib.Path, nargs="*", default=[], help="stories (.md) / prototypes (.html)")
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    rep = Report()
    facts = check_payload(args.skill, rep)

    docs = args.docs
    if docs is None:
        for up in (args.skill, *args.skill.parents):
            cand = up / "index.html"
            if cand.is_file():
                docs = cand
                break
    if docs and docs.is_file():
        check_docs(docs, facts, rep)
    else:
        rep.add(INFO, "D00", "no published guide found — docs parity skipped")

    if args.artifacts:
        catalog = args.skill / "references" / "lsc-standard-objects-catalog.md"
        names: set[str] = set()
        if catalog.is_file():
            # Multi-hump CamelCase only: "ProductionBatch" never appears in
            # business prose by accident, but "Visit" and "Product" do.
            for nm in re.findall(r"^\|\s*\*\*([A-Za-z][A-Za-z0-9_]*)\*\*\s*\|", read(catalog), re.M):
                if len(re.findall(r"[A-Z][a-z]+", nm)) >= 2:
                    names.add(nm)
        for p in args.artifacts:
            if not p.is_file():
                rep.add(WARN, "A00", "artifact not found", str(p))
            elif p.suffix.lower() == ".html":
                lint_prototype(p, rep)
            else:
                lint_story(p, rep, names)

    counts = rep.counts()
    if args.as_json:
        print(json.dumps({"facts": facts, "counts": counts,
                          "findings": [f.__dict__ for f in rep.findings]}, indent=2))
    else:
        for group, label in (("P", "PAYLOAD"), ("D", "DOCS"), ("A", "ARTIFACT")):
            rows = [f for f in rep.findings if f.code.startswith(group)]
            if not rows:
                continue
            print(f"\n{label}")
            for f in rows:
                mark = {FAIL: "FAIL", WARN: "warn", INFO: "  ok"}[f.level]
                print(f"  {mark}  {f.code}  {f.message}" + (f"  [{f.where}]" if f.where else ""))
        print(f"\n{counts[FAIL]} fail · {counts[WARN]} warn · {counts[INFO]} ok")

    return 1 if counts[FAIL] or (args.strict and counts[WARN]) else 0


if __name__ == "__main__":
    sys.exit(main())
