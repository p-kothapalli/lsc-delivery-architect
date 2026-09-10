# Story Output Template, Effort Sizing & Save Location (LSC)

The exact output format every generated LSC story must follow, plus effort sizing
and where to save the file. `SKILL.md` STEP 4 links here.

## Contents

- Canonical section order (required vs. optional)
- Full story template (copy and fill)
- Effort Sizing Guide (T-shirt + optional story points)
- Where to save the story

---

## Canonical section order

Every story appears in this exact order. **required** sections are always
present; _optional_ sections appear only when relevant.

1. Header (Persona, Priority, Sub-domain, **Surface**, **Offline**, Build Technology, OmniScript, IPs, Relevant Requirements, Veeva Source) — **required**
2. Story (As a / I want / So that) — **required**
3. Why it matters — **required**
4. Scope table (Flow, Component, Affected Step, Data Source) — _optional_
5. Current State (from codebase / Veeva) — _optional_
6. **Acceptance Criteria** (Patterns A–F — see `references/ac-pattern-library.md`; every "records created/updated" outcome carries a Pattern E per-object field spec, and every offline-iPad story carries at least one Pattern F offline/sync AC) — **required**
7. **Technical Implementation (high-level)** — **required**
8. Definition of done (checkbox list) — **required**
9. Clarification Questions table — **required when ambiguity exists**
10. Impact Analysis table — _optional_
11. Estimated Effort table — **required**

The Technical Implementation section sits between AC and Definition of done so
business reviewers can stop at the end of the AC block while developers continue.
Never interleave implementation details into the AC block.

---

## Full story template

Use this EXACT format. Every section is REQUIRED unless marked optional.

```
# USER STORY [N]: [Descriptive Title]

**Persona:** [Concrete LSC business role from the LSC Persona Cheatsheet — e.g. "Field Sales Representative". NEVER "business user"; never "HCP" for internal features.]
**Priority:** P[0-2]
**LSC Sub-domain:** [Commercial / Medical / Market Access / Cross-domain]
**Surface:** [iPad (online + offline) / iPad (online only) / Lightning web / Both — RULE 16. Default to iPad for field personas (Field Sales Rep, MSL, KAM, DSM, Event Organizer). See references/lsc-mobile-ipad.md]
**Offline:** [Required / Not required / N-A (web-only story) — if Required, the story MUST carry at least one Pattern F AC and the mobile Definition-of-Done items]
**Build Technology:** [Primary tech — Standard platform (Flow / Dynamic Actions / Action Launcher / Apex / LWC) and/or OmniStudio; if OmniStudio, note runtime: Standard vs managed package. Must be a technology that renders on the declared Surface]
**OmniScript / Flow:** [OmniScript or Screen Flow API Name(s) — or "N/A" / "Proposed (greenfield)"]
**Integration Procedures:** [IP names — or "N/A"]
**Relevant Requirements:** [Reference IDs, defect numbers, or requirement doc names]
**Veeva Source:** [Original Veeva object/feature this migrates from — omit if net-new]

---

## Story

**As a** [persona — same concrete role as above],
**I want** [specific capability described in business terms],
**So that** [measurable business outcome].

**Why it matters:** [1–2 sentences of business context explaining urgency or impact]

---

## Scope

| Flow | Component | Affected Step | Data Source |
|------|-----------|--------------|-------------|
| [Flow name] | [OmniScript / Screen Flow / FlexCard / Action Launcher] | [Step name] | [Data Mapper / IP / Apex / object that feeds it] |

---

## Current State (from codebase / Veeva)

### [Component or Veeva feature]

- **[Element]** ([Type]): [Current behavior — from actual codebase files, or the legacy Veeva behavior being replaced]
- **Location:** `[file path or Veeva object name]`

---

## Acceptance Criteria

> Every AC uses one of the six patterns from references/ac-pattern-library.md:
> A (behavioural GWT, business language), B (field/object/metadata bullets),
> C (permission set / FLS bullets), D (field update rules), E (record & field
> specification — per-object field recipe for created/updated records),
> F (offline / sync behaviour — on-device vs after-sync vs on-failure). No Apex
> class names, IP versions/step numbers, SOQL, or API field names inside
> Pattern-A ACs. Any "records are created/updated" outcome MUST include a
> Pattern E block enumerating every object and every field. Any story whose
> Surface includes offline iPad MUST include at least one Pattern F AC.

**AC-1 — [Short title in business language]**

**Given** [persona + business state — no technical jargon]
**When** [single business action]
**Then** [observable business outcome the persona can see or QA can verify]
**And** [optional additional outcomes, one per line]

**AC-2 — [Short title]**

[Use Pattern A, B, C, D, or E as appropriate. Include at least one happy path and
at least one edge case / negative path. Edge cases get their own AC.]

---

## Technical Implementation (high-level)

> Concise — one table or short bulleted list. NOT a re-spec of the ACs. Deep
> design notes live in a linked requirements/Enhancements/*_Architecture.md doc.

| Component | Type | Change | Notes |
|---|---|---|---|
| `<API name or file path>` | New Apex class / New IP / New Omnistudio Data Mapper / New Screen Flow / New custom field / Modified OmniScript / Dynamic Action / CMDT seed / Action Launcher action / **Object metadata cache config** / **Metadata cache regeneration** | One-line description of the change | Cross-ref to the AC it drives (e.g., "Drives AC-1") |

When Surface includes iPad, this table MUST include the mobile enablement rows —
the object metadata cache configuration (with its SOQL Filter Condition and
`Web-to-Mobile Sync` setting) and the cache regeneration for each affected
profile. Without them the change deploys successfully and remains invisible on
the device. See `references/lsc-mobile-ipad.md`.

If the story changes only a single component, a 3–5 bullet list is sufficient.

---

## Definition of done

> Verifiable outcomes, not activities. Cover happy path, key edge case(s),
> access/FLS if fields changed, and (for Apex) the >=85% coverage gate.
> When Surface includes iPad, the mobile block below is REQUIRED (RULE 16).

- [ ] [Primary behaviour from the happy-path AC is verified in the target org]
- [ ] [Key edge case / negative path from its AC is verified]
- [ ] [New fields/objects deployed with FLS applied per the permission-set AC, if applicable]
- [ ] [>= 85% Apex test coverage incl. bulk + negative paths, if Apex changed]
- [ ] [No regression to the flows named in Impact Analysis]

<!-- Include this block whenever Surface includes iPad. Delete for web-only stories. -->
- [ ] Behaviour verified in the **Life Sciences Cloud Mobile app on iPad**, not only in Lightning web
- [ ] Object metadata cache configuration created/updated for every new or changed object, with a SOQL Filter Condition set
- [ ] **Metadata cache regenerated** and the change confirmed visible on a device for **each affected profile** (the cache is profile-scoped)
- [ ] `Web-to-Mobile Sync` selected on objects whose web-side edits must reach the device
- [ ] Offline path verified: action performed with connectivity disabled, then synced, and the resulting records confirmed
- [ ] Sync failure path verified: `DeviceSyncTransaction.Status = Failed` with a diagnostic log entry, and **no end-user error shown to the rep**
- [ ] Layout and touch targets verified in iPad **landscape and portrait**

---

## Clarification Questions (Before Implementation)

| # | Question | Impact | Owner |
|---|----------|--------|-------|
| 1 | [Specific question] | [What it affects if answered differently] | [Technical / Commercial Ops / Medical / Compliance / Product] |

---

## Impact Analysis

| Component | Type | Impact Level | Description |
|-----------|------|-------------|-------------|
| [Name] | [OmniScript / Omnistudio Data Mapper / IP / Screen Flow / Apex / Object / LWC / Action Launcher / Dynamic Action] | [HIGH / MEDIUM / LOW] | [Why it's impacted] |

---

## Estimated Effort

| Component | Change Type | Effort | Notes |
|-----------|-----------|--------|-------|
| [Name] | [Picklist / OmniScript element / Omnistudio Data Mapper / IP / Screen Flow / Apex / LWC / Config] | [S/M/L/XL/XXL] | [Context] |

**Total Estimated Effort:** [Sum] — [T-shirt size overall]
```

---

## Effort Sizing Guide

| Size | Hours | Story Points | Description | Examples |
|------|-------|--------------|-------------|----------|
| **S** | < 1 hr | 1 | Config change, no code | Picklist value add, custom metadata record, permission set update |
| **M** | 2–4 hrs | 2 | Single component edit | OmniScript element change, Data Mapper field add, simple IP step change, Screen Flow tweak, Dynamic Action rule |
| **L** | 4–8 hrs | 3 | New component or multi-element change | New Omnistudio Data Mapper, new IP step, OmniScript step redesign, new Screen Flow, Action Launcher action |
| **XL** | 1–2 days | 5 | Complex logic or cross-component | New Apex class, complex IP chain, new OmniScript flow, LWC component, inventory reconciliation logic |
| **XXL** | 3+ days | 8+ | Multi-component integration | Cross-flow redesign, new object model, Veeva→LSC data migration, multi-system integration (Data Cloud, ERP) |

**Mobile surcharge.** A story targeting the iPad surface carries work a web-only
story does not: object metadata cache configuration, SOQL filter tuning, cache
regeneration per profile, offline-path testing, and device verification in both
orientations. Budget at least one extra **M** for mobile enablement, and treat
"same feature, but offline" as a size step up (offline capture with dependent
records and signature is rarely below **XL**). Never size an iPad story as if it
were the web story.

The **Story Points** column is optional but recommended when the story feeds a
GUS/agile backlog. Include a points total alongside the T-shirt total when the
user works in sprints; otherwise the T-shirt size alone is sufficient.

Label effort as "AI-estimated — validate with team" to set expectations.

---

## Where to Save the Story

Unless the user names a different path, write the generated story to:

- **Story file:** `requirements/<PascalCaseTitle>.md` (e.g.
  `requirements/LSC_SampleInventoryDashboard_UserStory.md`). Match the naming
  style of existing files in `requirements/`.
- **Deep architecture / design notes** (if a developer needs more than the
  concise Technical Implementation section): a separate
  `requirements/Enhancements/<Title>_Architecture.md`, linked from the story.
- **QTA prompts** (if generated): `qta_test_prompts.md` alongside the story.

Confirm the filename with the user if the topic overlaps an existing file
(append vs. create new). Never overwrite an unrelated existing story.
