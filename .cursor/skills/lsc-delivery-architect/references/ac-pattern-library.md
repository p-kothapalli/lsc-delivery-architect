# Persona & AC Authoring Contract + AC Pattern Library (LSC)

The two non-negotiables for every generated story: a concrete LSC business-role
persona, and acceptance criteria written in business language using one of five
patterns. This file is the authoritative detail for both; `SKILL.md` summarizes
and links here.

## Contents

- Persona rule (concrete LSC business role) + LSC Persona Cheatsheet + the HCP/HCO trap
- Given / When / Then contract (Pattern A rules + right/wrong examples)
- AC Pattern Library: Pattern A (behavioural), B (field/object/metadata),
  C (permission set / FLS), D (field update rules), E (record & field specification),
  F (offline / sync behaviour)
- "When in doubt" pattern-selection guide

---

## A) Persona must be a real, concrete LSC business role

The persona is the **Salesforce login user** who performs the action — a
commercial or medical field/office role — NOT the doctor or organization the work
is *about*.

| Don't write | Write instead |
|---|---|
| "As a business user" | "As a **Field Sales Representative**" |
| "As a user" | "As a **Medical Science Liaison (MSL)**" / "**Key Account Manager (KAM)**" / etc. |
| "As an HCP" (for an internal feature) | "As a **Field Sales Representative** visiting an HCP" (HCP is the subject) |
| "As a developer / business analyst" | Keep the business persona on the header; put developer-facing rules into Technical Implementation. |

### The HCP / HCO / KOL / DOL trap (LSC-specific)

- **HCP** (Health Care Provider), **HCO** (Health Care Organization), **KOL**
  (Key Opinion Leader), and **DOL** (Digital Opinion Leader) are the **subjects/
  targets** of the work — the accounts a field user visits, samples, or engages.
- They are the persona **only** when the story is genuinely for an HCP-facing
  experience (e.g. an Experience Cloud portal, a self-service consent capture, a
  patient/provider community). In that case name it: "As an **HCP portal user**".
- For everything internal, the persona is the field/medical/office role.

### LSC Persona Cheatsheet

Detected on first run by scanning `requirements/` and `permissionsets/` for role
labels. Canonical starter list (LSC):

The **Primary surface** column drives RULE 16 — it is the default Surface for a
story with that persona, unless the user says otherwise. See
`references/lsc-mobile-ipad.md`.

| Sub-domain / Context | Persona to use | Primary surface |
|---|---|---|
| Field sales visits, calls, sample drops | **Field Sales Representative** | **iPad (offline)** |
| Sample inventory / lot reconciliation / accountability | **Sample Accountability Manager** (or Field Sales Rep for on-hand) | iPad (rep) / web (manager) |
| Key account planning & strategy | **Key Account Manager (KAM)** | **iPad**, some web |
| Medical affairs, scientific engagement, KOL/DOL | **Medical Science Liaison (MSL)** | **iPad (offline)** |
| Medical information requests | **Medical Information Specialist** | Lightning web |
| Territory design, alignment, cycle plans | **Commercial Operations Analyst** (or Sales Operations Manager) | Lightning web |
| Payer / formulary / contracts | **Market Access Manager** | Lightning web |
| Content / approved email / CLM | **Marketing Operations Specialist** | Web (authoring) → iPad (delivery) |
| Compliance oversight (Sunshine Act, PDMA, consent) | **Compliance Specialist** | Lightning web |
| First-line field management | **District Sales Manager** | **iPad**, some web |
| Managed events / field events | **Event Organizer** | **iPad + web** (Offline Mobile is primary) |
| LSC setup, Admin Console, Concur settings | **LSC Admin** | Lightning web |

If the user names a persona that isn't in the cheatsheet, accept it verbatim and
add it to the story header. Prefer the workspace's established term over a casual
term when they conflict.

---

## B) Acceptance Criteria — Given / When / Then is mandatory

Every behavioural AC is **three explicit lines**, not a prose paragraph:

```
**AC-N — Short title**

**Given** [precondition / state before the action — be specific about objects, fields, picklist values, RecordTypes, account state]
**When** [the single trigger / action — usually one user action]
**Then** [the observable, verifiable outcome — record changes, field values, error messages, UI behavior]
**And** [optional additional outcomes, one per line]
```

Hard rules:

- One **When** per AC. If you have two actions, split into two ACs.
- The **Then** must be observable and checkable (QA can query, click, or read a
  log to confirm it). "It works" is not a valid Then.
- Use `**And**` lines for compound outcomes, not commas inside Then.
- Keep verbs in business language; implementation details belong in the
  Technical Implementation section.
- Edge cases get their own AC (Given = the edge state; Then = the
  rejection / fallback / log entry).
- If you write more than ~6 lines under a single Then, split the AC.
- **Qualify the surface in the Given whenever behaviour differs by surface**
  (RULE 16). Write "Given a Field Sales Representative **working offline in the
  LSC Mobile app on iPad**…" rather than leaving the device implicit. If the
  behaviour is identical on iPad and web, no qualifier is needed — but if it
  differs, an unqualified AC is untestable because QA can't tell which surface
  to test. Where several behaviours diverge, use the per-surface behaviour
  matrix in `references/lsc-mobile-ipad.md` instead of repeating ACs.

**Example — wrong (prose with technical jargon):**

> AC-1.1 When Submit fires, `LSC_SampleTxn_Procedure_4` calls
> `LSC_SampleAccountabilityService.reconcile(...)` before inserting the
> `SampleTransaction` record.

**Example — right (GWT in pure business language):**

```
**AC-1.1 — Sample drop reduces on-hand inventory**

**Given** a Field Sales Representative has on-hand quantity of a sample lot in
their inventory,
**When** they record a sample drop to an eligible, licensed HCP during a visit,
**Then** the disbursed quantity is deducted from their on-hand balance for that lot,
**And** the HCP's signature is captured against the sample transaction,
**And** the Field Sales Rep is never allowed to disburse more than their on-hand balance.
```

The implementation details (service class name, IP step numbers, SOQL) move to
the story's Technical Implementation (high-level) section.

---

## AC Pattern Library

Every AC uses ONE of six patterns. Pick the pattern that matches what the AC is
asserting; don't force a GWT shape on a metadata-spec AC.

### Pattern A — Behavioural AC (Given / When / Then) — DEFAULT

Use for: anything that asserts **system behaviour** the persona can observe — a
record gets created, a field gets updated, an error is shown, inventory changes,
a routing decision happens.

```
**AC-N — Short business-language title**

**Given** [persona + business state, no API names, no class names]
**When** [single business action]
**Then** [observable business outcome — what the persona sees, what business records change in business terms]
**And** [optional additional outcomes, one per line]
```

Keep the verbs in business language. Say "the on-hand balance is reduced", not
"`Quantity__c` is decremented". Say "a note is added to the visit", not "a
`Task` is inserted with `WhatId = visitId`".

### Pattern B — Field / Object / Metadata Creation

Use for: new custom fields, new custom objects, new Custom Metadata Types, new
field history tracking, new picklist values. These are inherently technical-spec
ACs — bullet structure is required, GWT is not.

```
**AC-N — Create following fields on [Object Label]**

- **API Name:** LSC_XxxYyy__c
- **Object:** [Salesforce object label / API name]
- **Type:** Checkbox / Text(80) / Lookup(Target) / Picklist / Master-Detail / etc.
- **Label:** [User-facing label]
- **Default:** [optional]
- **Help text:** [optional, customer-facing]
- **Description:** [optional, admin-facing]
- **Track History:** true / false
- **Required:** true / false (where applicable)
```

For new objects, add: Plural label, Sharing model, Auto-Number / Name format,
and a sub-list of fields using the same bullet style. For new Custom Metadata
Types, add a Seed-rows bullet describing how many rows and what governs the count.

### Pattern C — Permission Set / FLS

Use for: permission set updates, profile FLS, OWD changes, sharing rules.

```
**AC-N — Field Access & Permission Sets**

- **LSC_CommercialAdmin:**
  - Object level: Read, Create, Edit, View All Records
  - Field level: Read and Edit on all available fields
- **LSC_FieldSales:**
  - Object level: Read, Create, Edit
  - Field level: Read and Edit on the new fields
- **LSC_MedicalReadOnly:**
  - Object level: Read, View All Records
  - Field level: Read on all available fields
```

If only one permission set is affected and only one field is changing, you may
collapse into a single bullet, but keep the Object-level / Field-level split.

### Pattern D — Field Update Rules (business calculation tables)

Use for: ACs that describe **how** a value is computed when many conditional
branches feed it. Often appears inside the Then of a Pattern A AC, or as a
standalone "update rules" supporting block.

```
**AC-N — Update following records on [Object]**

**Given** [precondition],
**When** [action],
**Then** the following fields are set per the rules below:

- **Sample Eligibility =**
  - When HCP license is active AND state allows the product -> Eligible
  - When HCP license is expired -> Not Eligible (block disbursement)
  - Else -> Needs Review
- **On-Hand Quantity =** current On-Hand − disbursed quantity
- **Reconciliation Status =**
  - If physical count = system count -> Balanced
  - Else -> Discrepancy (flag for review)
```

This pattern is preferred over cramming six "And" lines into a single Then.

### Pattern E — Record & Field Specification (post-action record recipe) — MANDATORY when records are created/updated

Use for: any story where a Save, Submit, batch run, flow completion, or trigger
**creates or updates records** and the business team needs the *exact recipe* —
every object, every field, and the exact value (or formula) each is set to. One
block **per object**, listing **every field**, so a developer can build the write
without a follow-up meeting and QA can assert every field.

**Why mandatory:** a Pattern-A AC says *"the sample drop is recorded"* in
business language, but it does **not** tell the developer that
`Status = Submitted`, `Disbursement Date = TODAY`, `Signature Captured = true`,
etc. Whenever an AC's outcome is *"records are created/updated"*, pair it with a
Pattern E block that enumerates the fields.

**Structure — one sub-block per object, in creation/update order (parents before children):**

```
**AC-N — Records created/updated on <trigger> (outcome = <branch>)**

**Given** [precondition / which branch this recipe applies to],
**When** [the single trigger — Save / Submit / batch run / button click],
**Then** the following records are created/updated exactly as specified:

**<Object 1 — business label> — [Create | Update]**

| Field | Value | Notes |
|---|---|---|
| Record Type | Sample Disbursement | new / existing |
| Status | Submitted | |
| Disbursement Date | {TODAY} | |
| Account (HCP) | {Visited HCP} | lookup |
| Product | {Selected Product} | lookup |
| Quantity | {Disbursed Qty} | |
| ... every remaining field ... | ... | ... |

**<Object 2 — business label> — [Create | Update]**

| Field | Value | Notes |
|---|---|---|
| ... | ... | ... |
```

Hard rules for Pattern E:

- **List EVERY field** the record write touches — no "etc." / "and other fields".
- **One table per object.** Order objects the way they're written (parents
  before children) so the developer can follow the DML order.
- **Value column** holds the literal value, a `{merge/source}` placeholder in
  curly braces (e.g. `{Visited HCP}`, `{TODAY}`, `{Sample Lot}`), or a short
  formula. For multi-branch computed fields, nest the Pattern D rules in the
  Value cell or link to the Pattern D block.
- Use **business field labels**, not API names — the API-name mapping lives in
  the Technical Implementation table.
- If the same trigger produces **different recipes per branch**, give **each
  branch its own Pattern E AC** so QA can test each outcome independently.
- A "Create a Note / Call Report" instruction is a record write — spec it as its
  own object block.

### Pattern F — Offline / Sync Behaviour — MANDATORY when Surface includes offline iPad

Use for: any story whose **Surface** is *iPad (online + offline)* or *Both* with
offline required. Offline changes what "Then" means, because the outcome is
**deferred** — the rep's action succeeds on the device and the server write
happens later, possibly failing after the rep has walked away.

**Why mandatory:** a Pattern A AC that says *"Then the sample transaction is
recorded"* is ambiguous offline. Recorded **where** — on the device, or in
Salesforce? A rep who captured a signature in a basement office needs the device
to accept the work; the org needs the record to exist after sync; and the admin
needs a diagnosable failure if it doesn't. One Pattern A AC cannot carry all
three.

**Structure — three explicit phases:**

```
**AC-N — <Action> works offline and syncs on reconnect**

**Given** a <persona> is working **offline in the LSC Mobile app on iPad**,
**And** <the data the action depends on> has been primed to the device,
**When** they <single business action>,
**Then** ON DEVICE: <what the rep immediately sees — the action is accepted,
  the record appears in their local list, the running balance updates>,
**And** AFTER SYNC: <what exists in Salesforce once connectivity returns —
  which records, in which order>,
**And** ON SYNC FAILURE: <the transaction is marked failed for admin review;
  the rep is NOT shown a sync error>.
```

Hard rules for Pattern F:

- **Never show the rep a server-side or sync error.** They have no connectivity.
  Sync failures go to `DeviceSyncTransaction.Status = Failed` plus a
  `DeviceSyncTransactionLog` entry for admin monitoring. This mirrors the
  established Concur rule (integration errors are not end-user errors).
- **State what is primed.** If the Given depends on data being available
  offline, that data must be in the metadata cache. Name it, and cross-reference
  the cache configuration in Technical Implementation.
- **State validation feasibility.** A rule requiring a live query (real-time
  central inventory, an external licence lookup) **cannot** run offline. Say
  whether the data is primed or the rule degrades — don't leave it implied.
- **State ordering for dependent writes.** Where one offline record depends on
  another (visit → sample drop → signature), say the required order and what
  happens if the parent transaction fails. The platform carries this via
  `DependentOfflineIdentifiers` and `Sequence`; the AC states the business
  expectation.
- **Pair with Pattern E.** Offline still creates records. The Pattern E block
  specifies the fields; Pattern F specifies *when* they come into existence and
  what happens if they don't.
- **Cover conflict.** Give conflicting web-vs-offline edits on the same record
  their own AC, and say which side wins.
- **Timestamps are device-side.** `OfflineTimestamp` / `OfflineCreatedDate`
  record when the action *happened*, not when it synced. If the business cares
  about the actual interaction time (compliance, Sunshine Act reporting), say so.

**Worked example:**

```
**AC-4 — Sample drop captured offline syncs on reconnect**

**Given** a Field Sales Representative is working offline in the LSC Mobile app on iPad,
**And** their on-hand sample lots and the HCP's sampling eligibility were primed to the device at last sync,
**When** they record a sample drop with the HCP's signature during a visit,
**Then** ON DEVICE: the drop is accepted, the signature is stored with it, and their on-hand balance for that lot is reduced immediately,
**And** AFTER SYNC: the visit, the sample transaction, and the signature exist in Salesforce, written in that order, timestamped to when the drop actually occurred rather than when it synced,
**And** ON SYNC FAILURE: the transaction is flagged for administrator review with a diagnostic log entry, and the Field Sales Representative is shown no sync error.
```

Full offline authoring rules, the Device Sync object model, and the metadata
cache contract are in `references/lsc-mobile-ipad.md`.

### When in doubt

- A field, object, metadata type, or perm set is being **created or changed** (its *definition*) → Pattern B or C (structured bullets).
- The persona observes **behaviour** of the system → Pattern A (GWT).
- A computation has **many conditional branches** feeding a single outcome → Pattern D (rules block).
- A Save / Submit / batch / trigger **creates or updates record data** and you need the exact per-field recipe → Pattern E. **Always pair Pattern E with the Pattern A AC that describes the same action in business language.**
- The action happens **on the iPad with no connectivity**, so the outcome is deferred → Pattern F. **Always pair Pattern F with the Pattern E block that specifies the fields being written.**

See `references/story-examples.md` for worked exemplars (Patterns A–E). Pattern F
carries its worked example inline above.
