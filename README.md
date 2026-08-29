# LSC Delivery Architect

A reusable **Cursor skill** that acts as a Salesforce **Delivery / Solution
Architect** for **Life Sciences Cloud (LSC)** — and, uniquely, works
**prototype-first**: it can hand a Product Owner a *clickable, Salesforce-grounded
HTML mockup* + a lightweight *Solution Plan* **before** any user story is written,
then promote the plan into a full epic when the PO signs off.

It is the successor to the
[`lsc-user-story-architect`](https://github.com/p-kothapalli/lsc-user-story-architect)
skill. Same STEP 0–6 workflow and hard blockers; the identity was expanded to
match what the skill actually delivers today — **a Solution Plan, a grounded
prototype, or an implementation-ready user story, on demand and independently.**

**Working reference (GitHub Pages):**
[p-kothapalli.github.io/lsc-delivery-architect](https://p-kothapalli.github.io/lsc-delivery-architect/)
— a desk reference for solution architects, indexed by task rather than read
front-to-back:

| Tab | The question it answers |
|---|---|
| **Route Your Ask** | "I have *this* on my desk — which mode, and what do I paste?" |
| **Inside the Skill** | "What is actually baked in?" — the STEP 0–6 pipeline, the mode × phase skip matrix, all 17 critical rules *with their stated rationale*, the STEP 3 resolution order, and the 10-check STEP 5 validator loop |
| **Artifact Contract** | "What am I signing when I send this out?" — AC Patterns A–E, the persona cheatsheet, effort bands in hours, the DoD gates |
| **Build Decisions** | "Is this build-technology verdict defensible?" — the RULE 7a ladder plus a requirement-shape → verdict table |
| **LSC Lookups** | Filterable Veeva→LSC translation, compliance drivers, and the Commercial / Medical / Market Access object maps |
| **Repair & Review** | Symptom → cause → repair prompt for eight blocker failures, the 13 STOP tripwires verbatim, the rationalisation rebuttal table, plus pre-flight checklists for product owners and developers |

Start at **Route Your Ask** to install it and get a prototype in front of a
product owner. Come back to **Repair & Review** when output misses a blocker.

---

## Prototype-first, story-second

Traditional user-story generators force this order:

> _clarify → write story → argue about ACs → maybe build a mockup → build_

For most LSC engagements that's the wrong order. Product Owners consistently ask
two questions **before** they're ready to sign off on Given/When/Then ACs:

1. **"What will this actually look like on-screen?"**
2. **"Can we build it with OOTB Lightning, or do we need LWC / Flow /
   OmniStudio?"**

The LSC Delivery Architect answers both **first**, and only writes stories once
the PO has walked through the mockup and agreed to the shape.

### The three artifacts

| # | Artifact | When | Contract |
|---|----------|------|----------|
| **1** | **Solution Plan** | *"Plan this feature — no stories yet"* | Build-technology decision (declarative-first per RULE 7a), Component Inventory with badges + effort sizing, open questions. **No** ACs, **no** Pattern E — deliberately lightweight. |
| **2** | **Grounded HTML prototype** | *"Show me the built feature"* | Single self-contained `.html`, SLDS-flavoured, clickable state toggler, **every element badged** with the Salesforce component that will implement it (`OOTB` / `Config` / `Flow` / `LWC` / `OS` / `FC` / `IP` / `AL` / `Apex` / `Ext`), Build-Technology banner at top, component legend at bottom. |
| **3** | **Implementation-ready user story** | *"Promote this plan to stories"* — or start here | Concrete LSC persona, Given/When/Then ACs in business language, **Pattern E** per-field record spec on every write, Technical Implementation table, Definition of Done, Estimated Effort. |

Any one artifact, any combination, or all three — driven by the STEP 0 workflow
mode (`Plan + Prototype`, `New Feature`, `Refactor`, `Epic Breakdown`,
`Bug Fix`, or `Veeva → LSC Migration`).

---

## Grounded prototype hard blockers (§6.7)

The prototype is what separates this skill from a generic HTML mockup. It
**must**:

1. **State the Build Technology at the top** — the chosen tech + rationale +
   rejected alternative (declarative-first per RULE 7a).
2. **Label every interactive element** with the Salesforce component that will
   implement it — Lightning record page + Dynamic Actions, Screen Flow screen,
   LWC, OmniScript step, FlexCard, Action Launcher, Quick Action, related list,
   Path, etc.
3. **Distinguish OOTB vs. custom visually** — coloured badges per component
   type with hover-tips explaining the "why".
4. **Match the story's ACs and Pattern E field spec** (once stories exist) —
   every happy-path AC reachable in the click-through; forms show every field
   in the Pattern E table.
5. **Be a single self-contained `.html` file** — inline CSS, no external
   fonts/JS/CDN dependencies.
6. **Use SLDS-flavoured styling** so the mockup reads as *Salesforce*, not
   a generic web app.
7. **Include a Build-Technology legend footer** — component inventory with
   effort sizes mirroring the Solution Plan / story.
8. **Never invent component or field names** — custom components verified via
   `code-review-graph`, standard LSC objects/fields via `salesforce-docs`;
   unverifiable names marked `(proposed)`.

A prototype without the grounding is worse than no prototype — it misleads the
PO on cost shape. That's the whole point.

---

## What it produces (story mode, unchanged)

Every generated story follows one contract:

- **Concrete persona** — a real LSC role (Field Sales Rep, MSL, KAM, Event
  Organizer, LSC Admin, Market Access Analyst), never *"the user"*. HCPs are
  the *subject* of the work, not the login persona.
- **Given / When / Then** ACs in business language — no Apex class names, IP
  step numbers, SOQL, or `*__c` API names inside a GWT line.
- **Pattern E per-field record spec** on every "records created/updated"
  outcome — every field enumerated, no "etc.".
- **`## Technical Implementation (high-level)`** section after the ACs —
  a concise table naming components, change type, and a one-line note.
- **Definition of Done** and a **Clarification Questions** table for unknowns.
- **Estimated Effort** — component-level sizing (S / M / L / XL / XXL).
- **Grounded components** — custom verified via `code-review-graph`, standard
  LSC via `salesforce-docs`; proposals flagged when the LSC package isn't
  deployed in the target workspace (RULE 3a).

---

## What it knows (LSC knowledge pack)

- **Complete LSC standard-object catalog** — ~350 objects (Summer '26,
  API v67.0) grouped by functional domain, in
  [`references/lsc-standard-objects-catalog.md`](.cursor/skills/lsc-delivery-architect/references/lsc-standard-objects-catalog.md).
- **LSC object model** — Visits/Calls, Sample Management, Product Item &
  Production Batch inventory, Territory & MC Cycle Plans, Action Launcher,
  Assessments, **Medical Inquiry** (`Inquiry` / `InquiryQuestion` /
  `InquiryQuestionAnswer` — v65.0), Consent, KOL/DOL, Managed Events.
- **SAP Concur ⇄ LSC expense integration** — Visit **and** Event/Managed-Event
  expenses, the Expense / Expense Type / Expense Participant / Expense Report /
  Expense Report Entry (junction) model, `ExpenseSystemIntegrationStatus` sync +
  edit/delink matrix, actual-vs-estimated expenses, estimated allocation to
  participants, and the 1st-party MuleSoft "Concur Expense Sync" connector.
- **Declarative-first build-technology decision guide (RULE 7a)** — prefer
  OOTB Lightning + Dynamic Actions / Screen Flow / Field Sets before
  OmniScript; OmniStudio is *one* option, not the default. Standard vs.
  managed-package OmniStudio runtime call-out.
- **SLDS 2 primer** — token-driven design system reference for prototypes and
  future LWC work.
- **Veeva CRM → LSC migration** — terminology map + first-class migration
  workflow mode.

---

## Install

The skill lives under `.cursor/`, which Cursor auto-loads.

### Project-level (per repository) — recommended

```bash
# From the root of THIS repo, copy the .cursor payload into your target repo:
cp -R .cursor /path/to/your-project/

# or clone and copy:
git clone https://github.com/p-kothapalli/lsc-delivery-architect.git
cp -R lsc-delivery-architect/.cursor /path/to/your-project/
```

Reload the Cursor window. It activates automatically.

### User-level (available in every workspace)

```bash
cp -R .cursor/skills/lsc-delivery-architect ~/.cursor/skills/
cp    .cursor/rules/use-lsc-delivery-architect.mdc ~/.cursor/rules/
```

(Confirm the exact user-skills path in **Cursor → Settings → Rules &
Skills**.)

---

## Use

In a repo with the skill installed, just ask in natural language. The skill
routes to the right workflow mode via STEP 0.

### Prototype-first prompts (the new way — no stories yet)

- *"Plan and prototype `<capability>`."*
- *"Solution plan for `<capability>` — no stories yet."*
- *"Prototype-only for `<capability>` — we'll do stories after PO sign-off."*
- *"Just show me what the built feature would look like and what it costs."*

The skill produces:

1. `requirements/<Capability>_SolutionPlan.md`
2. `requirements/<Capability>_Prototype.html`

…then ends with **"Promote to Stories?"** — say the word and it switches to
Epic Breakdown mode and expands the plan into full user stories with ACs,
Pattern E, Technical Implementation, DoD, and QTA test prompts.

### Story-first prompts (unchanged from the sibling)

- *"Write an LSC user story for `<capability>`."*
- *"Break this LSC scope doc into stories."*
- *"Create a story to migrate `<Veeva feature>` to LSC."*
- *"Story for the Concur visit-expense integration."*
- *"Fix LSC Story: defect INQ-123 in `MSL_LogMedicalInquiry` — current: …,
  expected: …"*

### Post-generation offers (STEP 6)

Every generated artifact ends with a set of offers, gated by MCP availability:

- **6.1** QTA test-bridge prompts (once ACs exist)
- **6.2** Story / epic dependency diagram (udd-whiteboard / figma / Mermaid)
- **6.3** GUS work item creation
- **6.4** Salesforce Docs verification
- **6.5** Life Sciences Librarian notebook lookup (NotebookLM)
- **6.6** Story dependency check across `requirements/`
- **6.7** Grounded HTML prototype — first-class in Plan + Prototype mode,
  optional after a story

---

## Verify it loaded

Type either of these and confirm the skill activates:

- *"Plan and prototype a test capability — no stories yet"* → should route to
  Plan + Prototype mode and ask Phase 1 + Phase 2 clarifying questions only.
- *"Write an LSC user story for a test field"* → should ask 5–16 LSC clarifying
  questions via a structured multiple-choice picker.

---

## Optional: component grounding via MCP

For full structural grounding (caller/dependent/test context), configure the
`code-review-graph` MCP server in your `.cursor/mcp.json`. For standard LSC
object/field/feature verification with citations, configure the
`salesforce-docs` MCP. Without either, the skill still works — it falls back
to file search + curated references and clearly marks unverifiable names as
`(proposed)`.

---

## Repository layout

```
.cursor/
  skills/lsc-delivery-architect/
    SKILL.md                  # the skill (navigational overview, STEP 0–6)
    references/
      ac-pattern-library.md          # Persona contract + AC Patterns A–E
      output-template.md             # Full story template + effort sizing
      plan-prototype-mode.md         # Plan + Prototype (no stories) contract
      post-generation-offers.md      # STEP 6 detail — including §6.7 prototype
      lsc-object-model.md            # Curated LSC data model + acronyms
      lsc-standard-objects-catalog.md# All ~350 LSC standard objects (v67.0)
      lsc-components.md              # Build-tech decision guide + runtime call-out
      concur-integration.md          # SAP Concur ⇄ LSC expense integration
      veeva-to-lsc-mapping.md        # Veeva → LSC terminology + migration workflow
      slds2-lsc-primer.md            # SLDS 2 token / design-system primer
      story-examples.md              # Worked exemplars (Patterns A–E)
    evaluations/                     # Eval scenarios + rubric
  rules/
    use-lsc-delivery-architect.mdc   # Trigger rule
README.md
index.html                # GitHub Pages working reference (task-indexed)
```

---

## Version

See the **Version History** table in
[`SKILL.md`](.cursor/skills/lsc-delivery-architect/SKILL.md). The Plan +
Prototype mode landed in **v1.7** (Aug 2026); the skill was renamed from
"LSC User Story Solution Architect" to "LSC Delivery Architect" in **v1.8**
because *"user story"* no longer described what the skill actually delivers.

## Sibling / lineage

- Sibling (vertical-agnostic): [User Story Solution Architect](https://github.com/p-kothapalli/user-story-solution-architect) (if published)
- Predecessor (v1.0 – v1.7 under the old name):
  [`lsc-user-story-architect`](https://github.com/p-kothapalli/lsc-user-story-architect)
