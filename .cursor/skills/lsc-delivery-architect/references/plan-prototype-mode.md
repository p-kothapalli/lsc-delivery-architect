# Plan + Prototype mode (no stories)

> **Workflow mode:** `Plan + Prototype (no stories)` — introduced in `SKILL.md` v1.7.
> **Deliverable:** a lightweight **Solution Plan** artifact + a grounded HTML
> prototype (§6.7). **Not** a user story.
> **Purpose:** answer the product-owner ask *"Can I get a plan and a prototype
> now, and stories later?"* — without diluting the story-first contract for the
> other five workflow modes.

---

## When to use this mode

Use it when the requester wants a fast, product-owner-facing answer to
"**what will we build and roughly how big is it?**" — before the team is ready
to invest in Given/When/Then acceptance criteria and Pattern E per-field record
specs. Typical prompts:

- *"Give me a plan and a prototype for X."*
- *"I need a solution plan for X — no stories yet."*
- *"Prototype-only for X — we'll do stories after PO sign-off."*
- *"Just show me what the built feature would look like and what it costs."*

Do **not** use this mode when:

- The requester explicitly asked for stories, ACs, or a build spec → use
  **New Feature** / **Refactor** / **Epic Breakdown** / **Veeva → LSC Migration**.
- The team is ready to start coding → they need stories, not a plan.
- The change is a bug fix → use **Bug Fix**.

---

## Detection (natural language)

Route to this mode when any of these appear in the prompt:

- `"plan and prototype"`, `"plan + prototype"`
- `"plan only"`, `"just a plan"`, `"solution plan"`
- `"prototype only"`, `"prototype first"`
- `"no stories yet"`, `"not ready for stories"`, `"before stories"`
- Any phrasing that pairs "plan" and "prototype" without asking for stories.

Ambiguous phrasing (e.g. *"plan this feature"* on its own) → default to
**New Feature** and ask a clarifying question:
*"Do you want the full user story now, or just the Solution Plan + prototype
for now with stories to follow?"*

---

## Workflow (STEP 0–STEP 6 mapping)

| STEP | Behavior in this mode |
|------|----------------------|
| **0** | Detect this mode; announce it and confirm ("**Plan + Prototype mode — no stories will be written yet. OK?**"). |
| **1** | Full sub-domain selection (Commercial / Medical / Market Access / Cross-domain). Same as the story-first modes. |
| **2** | Ask **Phase 1 + Phase 2** clarifying questions only (context + business requirements). **Skip Phase 3–4** — they're calibrated for AC-level detail this mode doesn't produce. Cap at 6 questions. |
| **3** | **Full component verification.** Custom via `code-review-graph`; standard LSC via `salesforce-docs`. Cannot ground a prototype without this. |
| **4** | **Skip** story generation. Produce the **Solution Plan** artifact (template below) instead. |
| **5** | Run the review checklist — but only the items marked "retained" in the rules matrix below. |
| **6** | Offer the grounded HTML prototype (**§6.7 is now first-class, not optional**) and finish with the **Promote to Stories** offer (below). |

---

## Rules matrix — what applies, what doesn't

| Rule (from SKILL.md) | Applies in this mode? | Note |
|---|---|---|
| RULE 1 — Confirm LSC sub-domain first | **Yes** | STEP 1 runs unchanged. |
| RULE 2 — Ask clarifying questions before generating | **Yes, reduced** | Phase 1+2 only, max 6 questions. |
| RULE 3 — Never hallucinate component/object names | **Yes — hard blocker** | The prototype grounds on these names. |
| RULE 3a — Unverifiable = *proposed* | **Yes** | Same as story-first modes. |
| RULE 4 — Follow the output format | **Replaced** | Use the **Solution Plan template** below instead of the story template. |
| RULE 5 — Include Clarification Questions table | **Yes** | Same table format; block appears at the bottom of the plan. |
| RULE 6 — Scan `requirements/` for overlap | **Yes** | Prevents planning something that conflicts with an existing story. |
| RULE 7 — LSC naming conventions | **Yes** | New component names in the plan follow LSC conventions. |
| RULE 7a — Declarative-first build-technology decision | **Yes — hard blocker** | This is the whole point. |
| RULE 8 — Estimated Effort section | **Yes, simplified** | Component inventory carries per-component sizing; a rough epic total is added. Full multi-row Estimated Effort table not required. |
| RULE 9 — Detect workflow mode | **Yes** | STEP 0 detected this mode. |
| RULE 10 — Offer QTA test bridge | **No** | No ACs to convert. Offer once stories are promoted (see below). |
| **RULE 11 — Given / When / Then for every behavioural AC** | **NOT APPLIED** | This mode produces no ACs. Story-first blocker skipped. |
| RULE 12 — Concrete LSC persona | **Yes** | The Solution Plan still names the primary persona. |
| **RULE 13 — Business-language ACs** | **NOT APPLIED** | No ACs. |
| **RULE 14 — `## Technical Implementation (high-level)` section** | **NOT APPLIED** | Component inventory replaces it; the two overlap. |
| **RULE 15 — Pattern E per-field record spec on every write** | **NOT APPLIED** | Pattern E is a story-level contract; not required for a plan. Prototype forms may show representative fields, labelled as *illustrative, to be fully spec'd at story time*. |
| **§6.7 grounded HTML prototype hard-blockers (all 9)** | **YES — hard blocker** | Every item, including the SLDS 2 + Cosmos primer (`references/slds2-lsc-primer.md`), build-tech banner + per-element component labels. In this mode §6.7 is not optional; a prototype without them is worse than no prototype. |

**Read this literally:** you may generate a plan without ACs, without a Pattern
E field spec, and without a Technical Implementation table — but you may
**never** generate a prototype without the grounding contract.

---

## Solution Plan artifact template

Save to: `requirements/<Capability>_SolutionPlan.md`
Companion prototype: `requirements/<Capability>_Prototype.html`

```
# Solution Plan — <Capability name>

**Sub-domain:** Commercial | Medical | Market Access | Cross-domain
**Primary persona:** <concrete LSC role — e.g. Field Sales Rep, MSL, KAM,
Market Access Analyst, Event Organizer>
**Related HCP/HCO/KOL/DOL subject(s):** <who the work is about (not the login persona)>
**Priority:** P0 | P1 | P2
**Build Technology (decision):** <one-line summary — e.g. "OOTB Lightning
record page + Dynamic Actions + one Screen Flow + one small LWC">
**Rejected alternative(s):** <e.g. "OmniScript — overkill for a single-screen action">
**Prototype:** [<Capability>_Prototype.html](./<Capability>_Prototype.html)
**Mode:** Plan + Prototype (no stories yet)
**AI-estimated — validate with team.**

---

## Ask (verbatim)

> <the requester's original prompt, quoted>

## Solution shape (1 paragraph)

<Two to four sentences: who does what, on which record/flow, resulting in
which outcome. Business language. No API names.>

## Component inventory

| # | Component | Type | Change | Effort | Why chosen |
|---|-----------|------|--------|--------|------------|
| 1 | <Standard `HealthcareVisit` record page> | OOTB | Config (Dynamic Actions) | S | Standard object supports the flow with no code |
| 2 | <e-signature widget> | LWC | New | M | No OOTB e-signature; small custom component |
| 3 | <"Sample Drop" Screen Flow> | Flow | New | M | Declarative branching covers the validation |
| 4 | <atomic write transaction> | Apex | New | M | Multi-object write in a single transaction |
| 5 | <External Data Cloud lot feed> | Ext | Config | S | Existing DC ingestion pattern |

**Badges** — one of: `OOTB`, `Config`, `Flow`, `LWC`, `Apex`, `OS`, `FC`, `IP`, `AL`, `Ext`.

## Rough effort roll-up

| Bucket | Size |
|--------|------|
| Declarative (OOTB + Config + Flow) | <S/M/L> |
| Light code (LWC + Apex) | <S/M/L> |
| Integrations (Ext) | <S/M/L> |
| **Epic total (AI-estimated)** | **<S/M/L/XL>** |

## Open questions

| # | Question | Owner |
|---|----------|-------|
| 1 | <e.g. "Which e-signature vendor: DocuSign, native SF, custom?"> | Compliance |
| 2 | <e.g. "Is HCP licence data in Data Cloud today or on-prem?"> | Data Architecture |

## What this plan does NOT include (yet)

- Given / When / Then acceptance criteria
- Pattern E per-object per-field record specs
- Technical Implementation table (component inventory is the plan-level substitute)
- Definition of Done
- QTA test-bridge prompts

These are produced when the plan is promoted to full user stories (see below).

## Next step

Prototype is at `<Capability>_Prototype.html`. When the PO signs off on the
prototype, run:

> `Architect LSC Story: <Capability>` — or say "**promote this plan to stories**"

…to expand this plan into a full epic breakdown with ACs, Pattern E specs,
Technical Implementation, and Definition of Done.
```

---

## Promote to Stories offer (end of STEP 6)

After presenting the Solution Plan + prototype, always finish with:

```
Plan and prototype are ready. When you're set, I can:

  1. Promote this into a full user-story epic — one story per component
     in the inventory, with Given/When/Then ACs, Pattern E field specs,
     Technical Implementation, and Definition of Done. Same skill,
     Epic Breakdown mode.

  2. Convert the prototype's happy-path into a QTA browser-automation
     test prompt (once stories exist).

  3. Generate a dependency diagram of the epic (§6.2).

  Say "promote to stories" to run #1.
```

When the user says **"promote to stories"** (or equivalent):

1. Switch to the **Epic Breakdown** workflow mode.
2. Use the Component inventory as the story boundary set (one story per
   logical component group).
3. Re-open Phase 3+4 clarifying questions (technical discovery + acceptance)
   that were skipped in Plan + Prototype mode.
4. Now RULE 11, 13, 14, 15 apply — story-first hard blockers reactivate.
5. Cross-reference each story to the Solution Plan file.

---

## Common mistakes in this mode

| Mistake | Fix |
|---------|-----|
| Writing Given/When/Then ACs anyway | STOP — RULE 11 is not applied in this mode. If the requester wants ACs, they're in the wrong mode. |
| Producing a prototype without a Salesforce component label on every element | STOP — §6.7 hard blockers are the whole point of this mode. |
| Skipping the build-technology decision because "we don't know yet" | STOP — say what the leading candidate is and list the rejected alternative. That's the decision the PO wants. |
| Inventing a component name because it's a plan, not a story | STOP — RULE 3 still applies. Mark unverifiable components as *proposed*. |
| Producing a full Estimated Effort table with per-component sub-tasks | Not needed here — the Component inventory row's effort column is sufficient. Save the detailed table for story-time. |
| Forgetting the "Promote to Stories" offer | Every plan run ends with it — that's how this mode connects back to the story-first flow. |

---

## Cross-references

- `SKILL.md` STEP 0 workflow table (this mode is row 6) and detection triggers
- `references/post-generation-offers.md` §6.7 (grounded HTML prototype
  contract — applies in this mode as a **first-class** deliverable, not an offer)
- `references/slds2-lsc-primer.md` (**how** the prototype is styled — SLDS 2 +
  Cosmos hooks, utility classes, blueprint recipes, badge overlay,
  self-check)
- `references/output-template.md` (story-first template — used when this mode
  is promoted to Epic Breakdown)
- `references/ac-pattern-library.md` (Patterns A–E — activated only after
  promotion)
