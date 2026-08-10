# Post-Generation Offers (STEP 6 detail)

After presenting a validated LSC story, offer these optional next steps. Each one
depends on an MCP server or CLI being connected — check availability first with
the MCP tooling and only offer what is usable. If a server is present but needs
auth, mention that it can be authenticated first.

> **MCP tool names are fully qualified** as `server:tool` (e.g.,
> `code-review-graph:query_graph`). In this workspace the underlying server ID
> may be prefixed (e.g., `project-0-IBXQA-code-review-graph`); use the tooling to
> resolve the exact ID before calling.

## Contents

- 6.1 QTA Test Bridge (`qta-core`)
- 6.2 Diagram Generation (`udd-whiteboard` / `figma` / `diagram-beautifier` / Mermaid)
- 6.3 GUS Work Item Creation (`gus_server`)
- 6.4 Salesforce Docs Verification (`salesforce-docs`)
- 6.5 Knowledge Base (`notebooklm`)
- 6.6 Story Dependency Check
- 6.7 Product-Owner HTML Prototype (Salesforce-grounded)

---

## 6.1 QTA Test Bridge (`qta-core`)

If the `qta-core` MCP server is connected, offer to convert acceptance criteria
into QTA-compatible test prompts.

```
"This story has [N] acceptance criteria. Would you like me to generate
QTA browser automation test prompts from them?"
```

Mapping rules for AC -> QTA prompt:

| AC Section | QTA Prompt Section |
|-----------|-------------------|
| **Given** (precondition) | Navigation steps + setup context |
| **When** (user action) | Click, type, select interaction steps |
| **Then** (expected result) | Assertion / verification checks |
| OmniScript / component name | Target URL / flow identifier |

Example output:

```
QTA Test Prompt: "Open the LSC Commercial app. Navigate to the Sample Inventory
Dashboard. Verify that only active sample lots for the running user's location
are listed with lot number, on-hand quantity, and expiration date. Confirm an
expired lot is flagged and excluded from the disbursable total."
```

Generate one QTA prompt per acceptance criterion. Store in `qta_test_prompts.md`
alongside the story.

---

## 6.2 Diagram Generation

Offer a diagram of the story (and, for an epic breakdown, an end-to-end
dependency chain). Use whichever is available, in this order:

1. **`udd-whiteboard`** MCP — collaborative whiteboard diagram.
2. **`figma`** MCP — if the team maintains design/flow diagrams in Figma.
3. **`diagram-beautifier`** skill — to produce a polished diagram.
4. **Mermaid fallback** — embed a Mermaid diagram directly in the story markdown.

The diagram should show:
- The current user story as the highlighted node
- The previous story that feeds into it and the next story that depends on it
- The full epic chain across all generated stories (epic breakdown mode)
- Any shared systems/objects (Product Item, Territory, Data Cloud) connecting stories

---

## 6.3 GUS Work Item Creation (`gus_server`)

If the `gus_server` MCP is connected (or GUS CLI via `sf data` as a fallback),
offer to create a work item:

```
"The story is validated. Would you like me to create a GUS work item?"
```

Map story sections to GUS fields:
- Story -> `Description`
- Acceptance Criteria -> `Acceptance_Criteria__c`
- Priority -> `Priority`
- Persona -> Team assignment context

---

## 6.4 Salesforce Docs Verification (`salesforce-docs`)

If the Salesforce Docs MCP is connected (`salesforce-docs:salesforce_docs_search`
/ `salesforce-docs:salesforce_docs_fetch`), use it to verify any **standard**
Salesforce / Life Sciences Cloud object, field, feature, or API fact the story
relies on (Account/Person Account, Visit, Product Item, Production Batch, Sample
Transaction, Action Launcher, Territory) and cite the returned source URL. This
is the **primary** verification path for standard LSC facts in a PNM workspace
where the LSC package may not be deployed. Custom `LSC_*` components are still
verified via `code-review-graph`.

---

## 6.5 Knowledge Base (`notebooklm`)

If the `notebooklm` MCP is connected, use it to consult the shared **Salesforce
Life Sciences Librarian** notebook for LSC/HLS best practices, data models, and
implementation patterns when a story touches unfamiliar commercial or medical
territory. This is also where the JIRA-generation reference guidance lives.

---

## 6.6 Story Dependency Check

After generating, scan `requirements/` for stories that reference the same
components. Report any dependencies or conflicts:

```
"I found 2 existing stories that reference the same components:
  - LSC_SampleInventoryDashboard_UserStory.md
  This story depends on the Product Item model from that story and blocks the
  reconciliation story. Would you like me to add cross-references?"
```

---

## 6.7 Product-Owner HTML Prototype (Salesforce-grounded)

After a validated story, offer to generate a **single-file, clickable HTML
prototype** that shows the product owner what the built feature will look and
behave like — **grounded in a Salesforce build-technology decision**, not a
generic web mockup.

```
"Would you like me to generate a clickable HTML prototype of this story?
It will label each screen with the Salesforce component that will build it
(OOTB Lightning record page + Dynamic Actions, Screen Flow, LWC,
OmniScript + FlexCard) so you can see whether we can ship this with OOTB
or need LWC/Flow work."
```

### Why this offering exists (Product Owner point of view)

Product Owners repeatedly ask two questions the acceptance criteria alone
cannot answer:

1. **"What will this actually look like on-screen?"** — they need a clickable
   walkthrough, not just Given/When/Then.
2. **"Can we build this with OOTB Lightning, or do we need LWC / Screen Flow /
   OmniStudio?"** — they need to know the *cost shape* of the story before
   sizing it.

A generic HTML mockup answers (1) and misleads on (2). A Salesforce-**grounded**
prototype answers both — every visible element is annotated with the platform
mechanism that will realize it, and the "Build Technology" header up front tells
the PO whether this is a **declarative** build, a **light-code** build, or a
**custom-code** build.

### Hard requirements (blockers)

A prototype produced by this skill MUST:

1. **State the Build Technology at the top** — using the primer's
   `.lsc-build-banner` (§8). The banner text is the same value that appeared
   in the story's `Build Technology` header field (RULE 7a), with a one-line
   rationale and the rejected alternative.
2. **Label every interactive element** with the Salesforce component that will
   implement it, using the primer's **`.lsc-badge`** vocabulary (§8):
   `OOTB` / `Config` / `Flow` / `LWC` / `OS` / `Apex` / `Ext`.
3. **Match the story's ACs** — every happy-path AC in the story must be
   reachable in the click-through; the edge-case AC(s) should be linked from a
   secondary state (error banner, empty state, offline state).
4. **Match the story's Pattern E field spec (RULE 15)** — forms that create or
   update records must show every field listed in the Pattern E table, using
   the same labels/values, with the record's target object annotated
   (e.g., "creates `HealthcareVisit` + `VisitedParty` (Pattern E §1–§2)").
5. **Be a single self-contained `.html` file** — inline CSS + inline SVG icon
   sprite, no external fonts/JS/CDN dependencies. Portable so the PO can
   email it or open it from their desktop.
6. **Use SLDS 2 + Cosmos styling per `references/slds2-lsc-primer.md`.** Every
   prototype:
   - Opens with the primer's `:root { --slds-g-* … }` CSS variable block (§1).
   - Uses SLDS 2 utility classes (`slds-grid`, `slds-p-around_medium`,
     `slds-text-heading_small`, etc.) from the primer's §4.
   - Builds screens from the primer's blueprint recipes (§5): page header,
     path, tabs, card, form, data table, buttons, modal, alert, related list,
     empty state, action bar.
   - Uses the primer's LSC icon vocabulary (§6) inline as an `<svg><symbol>`
     sprite.
   - Applies component styles from the primer's §7.
   - Applies the LSC build-tech badge overlay from the primer's §8.
   - Passes the primer's §10 **10-point self-check** and records the score
     as an HTML comment at the top of the file (score-only rule — never
     block save, always record).

   **Do not** hand-invent SLDS class names. **Do not** ship generic
   Bootstrap/Material chrome. **Do not** import SLDS from a CDN — self-contained
   file only.
7. **Include a Build-Technology legend** — a footer or sidebar block that
   enumerates the components used, the effort size for each (S/M/L from the
   story's Estimated Effort table), and the OmniStudio runtime choice if
   OmniStudio is in scope.
8. **Never invent component or field names.** Reuse the exact names verified
   in STEP 3 (custom via `code-review-graph`, standard LSC via
   `salesforce-docs`); mark unverified names as `(proposed)` — same rule as
   the story itself (RULE 3 / 3a).
9. **Never redefine or override the primer's hooks or utilities.** The primer
   is the single source of truth for SLDS 2 + Cosmos in this workspace; a
   prototype that redefines `--slds-g-*` values or overrides `.slds-*` classes
   is not compliant.

### Structure

A minimum LSC prototype has:

| Region | Primer recipe | Salesforce grounding |
|--------|---------------|----------------------|
| **Global header strip** | §5.12 (`.slds-global-header`) | App name, running-user context |
| **Build-technology banner** | §8 (`.lsc-build-banner`) | Chosen tech + rationale + rejected alternative from the story |
| **Page header** | §5.1 (`.slds-page-header`) | The record page top — labelled `OOTB` when standard |
| **Path** (record process stages) | §5.2 (`.slds-path`) | Standard `OOTB · Path` |
| **Tabs** (record page sections) | §5.3 (`.slds-tabs_default`) | Standard `OOTB` tabs |
| **Main canvas** | Any combination of §5.4–§5.11 (card, form, table, buttons, modal, alerts, related list, empty state) | Each recipe labelled with its Salesforce component |
| **State toggler** (happy-path / edge-case / error / success) | Multi-file or in-page tabbed states | Mirrors the ACs |
| **Build-tech legend / footer** | Component inventory | Directly mirrors the story's Estimated Effort table |

### Screen-labelling conventions

Use the primer's `.lsc-badge` vocabulary (§8) on every interactive element:

| Badge | Meaning |
|-------|---------|
| `OOTB`   | Standard Salesforce, no config change |
| `Config` | Declarative — Dynamic Actions, Field Sets, Page Layout, custom field |
| `Flow`   | Screen Flow · Record-Triggered Flow · Subflow |
| `LWC`    | Lightning Web Component (custom code) |
| `OS`     | OmniScript step |
| `Apex`   | Apex trigger, invocable, controller |
| `Ext`    | External integration — MuleSoft · Concur · Data Cloud · e-signature |

Every badge carries a one-line caption explaining the "why" (e.g.
`<span class="lsc-badge flow">Flow · licence check</span>`).

### File placement

Save the prototype next to the story:

```
requirements/<StoryName>_Prototype.html
```

…and reference it from the story's `## Definition of done` section (add a
"Prototype reviewed with PO" checkbox).

### When NOT to use

- **Bug-fix stories** where the UI does not change — skip the prototype.
- **Pure backend / integration stories** (e.g. a MuleSoft Concur sync change) —
  a sequence diagram is a better artifact; offer 6.2 instead.
- **Stories that violate the AC-format or persona hard blockers** — fix the
  story before producing a prototype. A grounded prototype cannot rescue an
  ungrounded story.

### Handoff prompt template

When the user accepts this offer, produce the file, then say:

```
Prototype saved to requirements/<StoryName>_Prototype.html
Build technology: <e.g. OOTB Lightning record page + Dynamic Actions + one
Screen Flow>. Rejected alternative: <e.g. OmniScript — overkill for a
single-screen action>.

Open the file locally to click through the happy-path and edge-case states.
Every screen element is badged with the Salesforce component that will
implement it. Effort inventory is at the bottom of the file — it mirrors
the Estimated Effort table in the story.
```
