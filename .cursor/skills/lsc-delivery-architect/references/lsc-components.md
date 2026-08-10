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
- Component types
- OmniStudio runtime: Standard vs Managed Package
- OmniScript element types (common in LSC flows)
- Action Launcher (LSC guided actions)
- Naming conventions (LSC)
- References

---

## Build-technology decision guide (read first)

Pick the **lowest-complexity technology that meets the requirement**. LSC is a
standard-platform product first; OmniStudio is additive.

| The requirement is… | Prefer | Notes |
|---|---|---|
| A field-status-driven action/button on a record (Visit, Account) | **Dynamic Actions** + **Action Launcher** | Standard, no code. Action Launcher lists Flows, OmniScripts, and Quick Actions. |
| A short guided form / quick capture | **Screen Flow** | Declarative, native, Agentforce/mobile friendly. |
| A complex, branching, multi-step **guided interaction** (offline field capture, signature, matrices) | **OmniScript** | Where OmniStudio earns its place; extend with custom LWC only for edge cases. |
| Rich, config-driven **data display** / launch tiles | **FlexCard** *or* custom **LWC** | LWC if you need full control; FlexCard for declarative config. |
| Reusable **server-side orchestration** (chain reads/writes, callouts, decisioning) | **Integration Procedure** | The reusable service layer for OmniScripts/FlexCards/LWCs. |
| Read / reshape / write Salesforce data **declaratively** | **Omnistudio Data Mapper** | Formerly DataRaptor. Prefer Turbo Extract for single-object reads. |
| Eligibility / routing / tiering lookup tables | **Decision Matrix** (Business Rules Engine) | BRE requires OmniStudio. |
| Custom business logic, bulk jobs, integrations, complex validation | **Apex** | Triggers, services, selectors, batchable/queueable. |
| Page layout, tabs, related lists, list views | **Lightning App Builder** + managed-package LWCs (e.g. *Related List — Life Sciences*, *Multi-Object Record*) | Standard config; reuse the LSC package components. |

Rule of thumb: **declarative-first (Flow / Dynamic Actions / Action Launcher /
Field Sets) → OmniStudio for genuinely guided or orchestrated needs → Apex/LWC
for logic and custom UI.** Note the chosen technology (and *why*) in the story's
Technical Implementation section.

---

## Component types

| Component | What It Is | When to Use | Runtime |
|-----------|-----------|-------------|---------|
| **OmniScript** | Multi-step guided UI flow (OmniStudio) | Complex/branching guided visit/sample flows, offline capture, signature | Client-side (LWC) |
| **FlexCard** | Config-driven data-display component (OmniStudio) | Record display, dashboards, inventory tiles, embed in OmniScript | Client-side (LWC) |
| **Integration Procedure (IP)** | Server-side orchestration (OmniStudio) | Chain Data Mappers, Apex, callouts, matrices; reusable service layer | Server-side |
| **Omnistudio Data Mapper** | Declarative read/transform/write (OmniStudio; **formerly DataRaptor**) | Fetch/reshape/save data without code. **Types: Turbo Extract, Extract, Load, Transform** | Server-side |
| **Decision Matrix** | Lookup/rule table (Business Rules Engine — requires OmniStudio) | Eligibility, routing, tiering | Server-side |
| **Screen Flow** | Standard guided screens | Short guided forms, quick capture; Action-Launcher target | Client-side |
| **Action Launcher** | Guided-action launcher on a record | Launch Flows/OmniScripts/Quick Actions from Visit, Account, etc. | Client-side |
| **Dynamic Actions** | Status/criteria-driven actions on a Lightning record page | Show only the actions relevant to record status/device | Client-side |
| **LWC** | Lightning Web Component | Custom UI (dashboards, timelines); reuse LSC package LWCs where possible | Client-side |
| **Apex** | Business logic (service / selector / trigger / batch) | Inventory reconciliation, eligibility, callouts, bulk jobs | Server-side |
| **Field Set** | Admin-configurable field grouping | Related-list / list-view column config in LSC package components | Config |

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
