# LSC Component & Naming Reference

Component technologies used in LSC stories, plus the naming conventions to apply
to any **new** component. Verify **existing** components via `code-review-graph`;
verify **standard LSC** features via `salesforce-docs`.

> **Audit note (verified Aug 2026 against Salesforce Help).** OmniStudio **is**
> part of Life Sciences Cloud — see
> [Omnistudio for Life Sciences Cloud](https://help.salesforce.com/s/articleView?id=ind.lsc_omnistudio.htm)
> — but it is **one option, not the default**. Modern LSC ships as managed
> packages (e.g. Life Sciences Customer Engagement, `lsc4ce__`) built on the
> **standard Salesforce platform**: Lightning record pages + **Dynamic Actions**,
> **Action Launcher**, **Screen Flows**, **Apex**, custom **LWCs**, **Field
> Sets**, and custom Labels. Choose the build technology per the **decision guide**
> below — don't assume every guided interaction is an OmniScript. Also: OmniStudio
> **DataRaptor was renamed "Omnistudio Data Mapper"** (Spring '24); prefer the new
> name.

## Contents

- Build-technology decision guide (read first)
- Surface constrains the decision (iPad vs web)
- Component types
- Mobile enablement: the metadata cache step
- OmniStudio runtime: Standard vs Managed Package
- OmniScript element types (common in LSC flows)
- Action Launcher (LSC guided actions)
- Naming conventions (LSC)
- References

---

## Build-technology decision guide (read first)

Pick the **lowest-complexity technology that meets the requirement** — **that
also runs on the story's declared Surface** (RULE 16). LSC is a
standard-platform product first; OmniStudio is additive.

| The requirement is… | Prefer | Mobile (iPad app) | Notes |
|---|---|---|---|
| A field-status-driven action/button on a record (Visit, Account) | **Dynamic Actions** + **Action Launcher** | **Yes — device-aware** | Standard, no code. Dynamic Actions can vary by **device**; toggle at Admin Console → Mobile → Application Settings. |
| A short guided form / quick capture | **Screen Flow** | **Yes — preferred on mobile** | Declarative, native. Flows are named in the LSC Mobile extension model. |
| A complex, branching, multi-step **guided interaction** (signature, matrices) | **OmniScript** *(web)* / **Screen Flow + LWC** *(iPad)* | ⚠️ **Verify** | See the surface note below — do **not** assume OmniScript runs in the LSC Mobile app. |
| Rich, config-driven **data display** / launch tiles | **FlexCard** *or* custom **LWC** | LWC yes (see naming); FlexCard ⚠️ verify | LWC if you need full control; FlexCard for declarative config. |
| Reusable **server-side orchestration** (chain reads/writes, callouts, decisioning) | **Integration Procedure** | Online only | Server-side — unavailable offline by definition. |
| Read / reshape / write Salesforce data **declaratively** | **Omnistudio Data Mapper** | Online only | Formerly DataRaptor. Prefer Turbo Extract for single-object reads. |
| Eligibility / routing / tiering lookup tables | **Decision Matrix** (Business Rules Engine) | Online only | BRE requires OmniStudio. Offline eligibility must be primed to the device instead. |
| Custom business logic, bulk jobs, integrations, complex validation | **Apex** | **Yes (server-side, on sync)** | Apex is named in the LSC Mobile extension model. Runs when the device syncs, not while offline. |
| Page layout, tabs, related lists, list views | **Lightning App Builder** + managed-package LWCs (e.g. *Related List — Life Sciences*, *Multi-Object Record*) | Yes — **requires metadata cache regeneration** | Standard config; reuse the LSC package components. |
| Data must be **available with no connectivity** | **Object metadata cache config** (+ SOQL filter, Web-to-Mobile Sync) | **Required** | Not a UI technology — the priming layer everything offline depends on. See below. |

Rule of thumb: **declarative-first (Flow / Dynamic Actions / Action Launcher /
Field Sets) → OmniStudio for genuinely guided or orchestrated needs → Apex/LWC
for logic and custom UI.** Note the chosen technology (and *why*) in the story's
Technical Implementation section.

---

## Surface constrains the decision (iPad vs web)

**Read this before choosing a technology for any field-persona story.** LSC ships
a dedicated **offline-enabled iPad app** that is the primary surface for Field
Sales Reps, MSLs, KAMs, DSMs, and Event Organizers. A technology that does not
render there is not a candidate, no matter how well it fits the requirement.
Full detail in `references/lsc-mobile-ipad.md`.

**Prefer on mobile:** Screen Flow, Apex, LWC, Dynamic Actions, standard record
pages. Salesforce's own positioning for the app is *"Native on the Salesforce
Platform — **Flows, Apex, and open APIs** for limitless extension."*

> ⚠️ **Correction to earlier guidance (was v1.5–v1.9).** This guide previously
> routed *"offline field capture, signature"* straight to **OmniScript**. That is
> not safe as a default: OmniStudio is supported **in LSC**, but Salesforce's
> LSC Mobile material does not name OmniScript as a mobile extension path.
> **Verify mobile support before proposing OmniStudio for an iPad-targeted
> story**, and record the verification in the Clarification Questions table.
> For offline guided capture on iPad, start from **Screen Flow + LWC + Apex**.

**Server-side technologies (IP, Data Mapper, Decision Matrix, Apex) do not run
while the device is offline.** They execute when the transaction syncs. Any
validation the rep must see *at the moment of capture* has to be local, which
means the data it depends on must be primed into the metadata cache. If it
can't be primed, the rule degrades offline — say so explicitly in the AC rather
than implying real-time behaviour.

---

## Component types

| Component | What It Is | When to Use | Runtime | iPad app |
|-----------|-----------|-------------|---------|---------|
| **OmniScript** | Multi-step guided UI flow (OmniStudio) | Complex/branching guided visit/sample flows, signature | Client-side (LWC) | ⚠️ **Verify** |
| **FlexCard** | Config-driven data-display component (OmniStudio) | Record display, dashboards, inventory tiles, embed in OmniScript | Client-side (LWC) | ⚠️ Verify |
| **Integration Procedure (IP)** | Server-side orchestration (OmniStudio) | Chain Data Mappers, Apex, callouts, matrices; reusable service layer | Server-side | Online only |
| **Omnistudio Data Mapper** | Declarative read/transform/write (OmniStudio; **formerly DataRaptor**) | Fetch/reshape/save data without code. **Types: Turbo Extract, Extract, Load, Transform** | Server-side | Online only |
| **Decision Matrix** | Lookup/rule table (Business Rules Engine — requires OmniStudio) | Eligibility, routing, tiering | Server-side | Online only |
| **Screen Flow** | Standard guided screens | Short guided forms, quick capture; Action-Launcher target | Client-side | **Yes — preferred** |
| **Action Launcher** | Guided-action launcher on a record | Launch Flows/OmniScripts/Quick Actions from Visit, Account, etc. | Client-side | Yes |
| **Dynamic Actions** | Status/criteria-driven actions on a Lightning record page | Show only the actions relevant to record status/device | Client-side | **Yes — device-aware** |
| **LWC** | Lightning Web Component | Custom UI (dashboards, timelines); reuse LSC package LWCs where possible | Client-side | **Yes** (mobile-ready; see naming) |
| **Apex** | Business logic (service / selector / trigger / batch) | Inventory reconciliation, eligibility, callouts, bulk jobs | Server-side | **Yes**, on sync |
| **Field Set** | Admin-configurable field grouping | Related-list / list-view column config in LSC package components | Config | Yes — needs cache regen |
| **Object metadata cache config** | Per-object mobile priming rule (type, SOQL filter, Web-to-Mobile Sync, attachment method) | Making any object visible / editable / offline-available on the iPad | Config | **Required for mobile** |

---

## Mobile enablement: the metadata cache step

**Every iPad-targeted story that touches schema needs this, and it is the single
most commonly missed deliverable.** The LSC Mobile app does not read org metadata
live — it works from a generated, **profile-scoped** cache.

Per [Mobile App Configuration for Visit Management](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_db_schema_metadata_cache.htm&type=5):

1. Create an **object metadata cache configuration** for each object the app must
   see (type is typically `Data`).
2. Select **Web-to-Mobile Sync** where web-side edits must reach the device.
3. Set a **SOQL Filter Condition** to bound what downloads to the device.
4. Set the **attachment download method** where relevant (e.g. `Cache` on `Visit`
   when a related list is configured).
5. **Generate the metadata cache** — Salesforce flags this as *Important*;
   without it, schema changes never reach the app.

> A new field deployed without a cache regeneration is **invisible on the
> device**: the deploy succeeds, the web UI shows the field, and the rep never
> sees it. Put the cache rows in Technical Implementation and the verification in
> Definition of done. Full detail: `references/lsc-mobile-ipad.md`.

> **Data Mapper types.** **Turbo Extract** — fastest single-object read (default
> for simple reads); **Extract** — multi-object read; **Load** — create/update/
> upsert; **Transform** — reshape JSON (incl. JSON↔XML). The legacy name
> "DataRaptor" still appears in APIs, object fields, and URLs, so existing
> components may carry it — use "Data Mapper" in new story prose.

---

## OmniStudio runtime: Standard vs Managed Package

A first-class question for any LSC OmniStudio story — it changes objects, tooling,
deployment, naming, and feature availability. **Ask/confirm which runtime the org
uses** and default new work to **Standard runtime**.

| Area | **Standard runtime** (recommended) | Managed Package runtime (Vlocity, legacy) |
|---|---|---|
| Status | Strategic direction; all new features; **Agentforce + Data Cloud integration** | Maintenance mode — no new features |
| Data model | Standard objects (`OmniProcess`, `OmniUiCard`, `OmniDataTransform`, …) | Namespaced custom objects (`vlocity_cmt__*`) |
| Designer | Standard OmniStudio Designer | Legacy (Vlocity Digital Studio) wrappers |
| Deployment | **Salesforce CLI / metadata API** (never Change Sets) | Omnistudio Build Tool (VBT) |
| Migration | — | Move to Standard runtime (OmniStudio Migration Assistant); **required for Agentforce** |

Best practice: **new LSC OmniStudio components target Standard runtime.** If the
target org is still on managed-package runtime, flag it (and any migration
implication) in the Clarification Questions table.

---

## OmniScript element types (common in LSC flows)

| Element Type | Purpose | Example (LSC) |
|-------------|---------|---------------|
| **Step** | Container grouping form elements | `RecordSampleDropStep` |
| **Type Ahead** | Autocomplete search | HCP account search |
| **Select** | Dropdown/picklist | Product / lot selector |
| **Edit Block** | Table/grid of records | Sample lines by lot |
| **Set Values** | Assign data to the OmniScript JSON | Default disbursement date |
| **Data Mapper Post Action** | Save via a **Load** Data Mapper (formerly DataRaptor Post) | Save sample transaction |
| **Data Mapper Extract Action** | Read via **Extract/Turbo Extract** | Load on-hand lots |
| **IP Action** | Invoke an Integration Procedure | Reconcile inventory |
| **Remote Action** | Call an Apex method | Validate HCP eligibility |
| **Signature** | Capture signature | HCP signature on sample drop |
| **Navigate Action** | Redirect on completion | Return to Visit record |
| **Conditional** | Show/hide logic | Show only if licensed to sample |
| **Custom LWC** | Embed a custom LWC (extends `OmniscriptBaseMixin` to talk to the script) | Custom inventory picker |

---

## Action Launcher (LSC guided actions)

LSC surfaces guided quick actions (record a visit, drop a sample, initiate a
product request) via **Action Launcher** on records like Visit or Account.
Action Launcher lists **Salesforce Flows, OmniScripts, and Quick Actions**. When
a story asks for a "quick action" or "button on the record", model it as an
Action Launcher entry that launches a **Flow or OmniScript** — name the launched
component, not a raw button — and pair it with **Dynamic Actions** if visibility
must depend on record status/device (e.g. show *Unlock* only when `Status =
Completed`). For structured, Apex-backed request flows, consider **Service
Process Studio / Service Process Definitions** (request form = OmniScript *or*
Screen Flow, plus an Apex preprocessor, Integration Definition, and optional
fulfillment flow).

---

## Naming conventions (LSC)

Apply an `LSC_` prefix to new custom components in a net-new LSC build. If the
target org already uses a customer-specific or managed-package prefix (e.g.
`lsc4ce__`), prefer that and note the choice in a Clarification Question. Standard
runtime favors **PascalCase**; establish the convention before the first
component.

| Component | Pattern | Example |
|-----------|---------|---------|
| OmniScript | `LSC_[FlowName]` (+ Type/SubType/Language, e.g. `_English`) | `LSC_RecordSampleDrop_English` |
| Data Mapper — Extract/Turbo Extract | `LSCDM Extract[Object][Context]` | `LSCDMExtractProductItemInventory` |
| Data Mapper — Load | `LSCDM Load[Object][Context]` | `LSCDMLoadSampleTransaction` |
| Data Mapper — Transform | `LSCDM Transform[Context]` | `LSCDMTransformSamplePayload` |
| Integration Procedure | `LSC_[Name]` | `LSC_InventoryReconciliation` |
| Parent IP | `LSC_[Name]Parent` | `LSC_SampleDropParent` |
| FlexCard | `lsc[ComponentName]` | `lscSampleInventoryCard` |
| LWC | `lsc[ComponentName]` | `lscInventoryTimeline` |
| LWC — **inline on a mobile record page** | `lscMobileInline_[ComponentName]` ⚠️ *(to verify)* | `lscMobileInline_CompetitorInsights` |
| Screen Flow | `LSC_[Name]` | `LSC_LogMedicalInquiry` |
| Apex service | `LSC_[Name]Service` | `LSC_SampleAccountabilityService` |
| Apex selector | `LSC_[Object]Selector` | `LSC_ProductItemSelector` |
| Custom Metadata | `LSC_[Name]__mdt` | `LSC_SampleEligibility__mdt` |
| Custom Field | `LSC_[FieldName]__c` | `LSC_OnHandQuantity__c` |
| Set Values Element | `SV_[Name]` | `SV_DisbursementDefaults` |
| IP Action Element | `IP[Name]` | `IPReconcileInventory` |

> The legacy `LSCDRExtract…` / `LSCDRUpdate…` ("DR" = DataRaptor) pattern still
> works — APIs keep the `dataraptor` token — but prefer the `LSCDM…` (Data
> Mapper) form for new components.

> ⚠️ **`lscMobileInline_` is unverified.** A custom LWC reportedly needs this
> API-name prefix to render **inline on a record page inside the LSC Mobile
> app**. The available sourcing is Agentforce Life Sciences Consultant
> (ALS-Con-201) certification material that cites Salesforce Help rather than
> Help itself, and the `salesforce-docs` MCP was unavailable when this was
> written. **Confirm against Salesforce Help before relying on it**, and mark it
> *(to verify)* in any story that proposes an inline mobile LWC.

Prefer **standard LSC objects/fields** over new custom ones; only introduce
`LSC_*` custom metadata/fields when the standard model cannot carry the
requirement.

---

## References

Verified against Salesforce Help / Trailhead (Aug 2026):

- [Omnistudio for Life Sciences Cloud](https://help.salesforce.com/s/articleView?id=ind.lsc_omnistudio.htm) — OmniStudio components available in LSC; required for Business Rules Engine & Decision Explainer.
- [OmniStudio Standard component reference](https://help.salesforce.com/s/articleView?id=xcloud.os_omnistudio_standard.htm&type=5)
- [Get to Know Omnistudio and Its Features (Trailhead)](https://trailhead.salesforce.com/content/learn/modules/omnistudio-development-essentials/get-to-know-omnistudio-and-its-features) — Standard vs Managed Package runtime; Data Mapper types.
- OmniStudio Summer '24 release notes — *DataRaptor is now Omnistudio Data Mapper*.
- [Add Actions with Dynamic Actions (LSC Visit Management)](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_add_actions_with_dynamic_actions.htm) — Dynamic Actions on the Visit record page.
- [Create and Activate Service Process Definitions](https://help.salesforce.com/s/articleView?id=ind.spd_create_service_process_definitions.htm) — OmniScript/Flow + Apex preprocessor via Service Process Studio.
- [Mobile App Configuration for Visit Management](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_db_schema_metadata_cache.htm&type=5) — object metadata cache, Web-to-Mobile Sync, SOQL Filter Condition, cache generation.
- [Life Sciences Cloud Mobile (App Store)](https://apps.apple.com/us/app/life-sciences-cloud-mobile/id6499238627) — the iPad app; "Native on the Salesforce Platform — Flows, Apex, and open APIs for limitless extension".
- `references/lsc-mobile-ipad.md` — surface decision, Device Sync object model, offline authoring rules.
