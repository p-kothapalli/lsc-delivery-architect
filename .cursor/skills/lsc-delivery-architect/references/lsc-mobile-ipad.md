# LSC Mobile (iPad) & Offline Reference

**Load this whenever a story's persona is a field-facing LSC role** — Field Sales
Representative, MSL, KAM, District Sales Manager, Event Organizer — because for
those personas the **iPad app is the primary surface, not a companion to the web
app**. A story written only for Lightning web is, for these users, a story for a
device they don't carry.

> **Why this file exists.** Through v1.9 the skill treated LSC as a desktop-web
> product. Surface appeared in exactly one place (`concur-integration.md`'s
> "Platform, offline & attachment rules"), which only loads for expense stories.
> v1.10 promotes surface to a first-class axis alongside build technology.

## Contents

- The product reality (what the iPad app is)
- Surface decision: which surface does this story target?
- The mobile metadata cache — the step everyone forgets
- Device Sync object model (offline transaction pipeline)
- Offline authoring rules (how offline changes an AC)
- Per-surface behaviour matrix
- Build technology on mobile
- Personas and their primary surface
- Definition-of-Done additions for mobile stories
- Clarification questions to ask
- Verified references

---

## The product reality

**Agentforce Life Sciences** (formerly Life Sciences Cloud — Salesforce renamed
it; see the [developer guide overview](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_cloud_overview.htm))
ships a **dedicated native iPad application**, distinct from the Salesforce
mobile app:

| Fact | Detail |
|---|---|
| App | **Life Sciences Cloud Mobile** — [App Store](https://apps.apple.com/us/app/life-sciences-cloud-mobile/id6499238627) |
| Platform | **iPadOS only** (the App Store listing requires iPadOS; there is no equivalent desktop-parity phone experience) |
| GA | The Life Sciences Cloud for Customer Engagement add-on SKU including the App Store app has been GA since **October 2025** |
| Offline | **Fully offline-capable** — "Prepare, engage, and stay compliant — even when completely offline." Offline analytics, offline visit capture, offline sample drops |
| Extensibility | "Native on the Salesforce Platform — **Flows, Apex, and open APIs** for limitless extension" |
| Licence | Enterprise/Unlimited + **Life Sciences Cloud for Customer Engagement Add-on** licence + the **Life Sciences Customer Engagement managed package** |
| Admin home | A dedicated **Admin Console → Mobile** area (e.g. *Application Settings → Enable Dynamic Actions*) |

Salesforce markets "**Offline-enabled iPad App**" as a headline capability of
[LSC for Customer Engagement](https://www.salesforce.com/life-sciences/cloud/customer-engagement/),
alongside Sample Management, CLM, and Territory Management. Offline is the
product's differentiator against Veeva, not an edge case.

> **Naming.** Salesforce now brands this **Agentforce Life Sciences**. This skill
> still uses "LSC" throughout for continuity with existing `requirements/` files.
> Use the customer's term in story prose; note the rename if a story references
> product marketing.

---

## Surface decision: which surface does this story target?

Ask this in **Phase 2** (business requirements), not Phase 4. It is a scoping
decision that constrains the Phase 3 build-technology choice — a technology that
doesn't render on the iPad app is not a candidate.

| Surface value | Means | Typical stories |
|---|---|---|
| **iPad (online + offline)** | Runs in the LSC Mobile app, must work with no connectivity | Visit execution, sample drop + signature, CLM/eDetailing, call reporting in the field |
| **iPad (online only)** | Runs in the LSC Mobile app but may require connectivity | Real-time inventory lookup, remote/video engagement, live approval |
| **Lightning web** | Desktop/browser only | Territory design, cycle plan authoring, admin config, expense report deletion, analytics authoring |
| **Both** | Must work on iPad *and* web, possibly with different affordances | Medical inquiry logging, expense capture |

Record the answer in the story header as **Surface** and **Offline**
(see `output-template.md`). If the answer is *iPad* or *Both*, this file's rules
apply and the story is incomplete without them.

**Default when unstated:** if the persona is field-facing (Field Sales Rep, MSL,
KAM, DSM, Event Organizer) and the user hasn't said otherwise, assume
**iPad (online + offline)** and confirm it as a clarifying question. Do **not**
silently default to web.

---

## The mobile metadata cache — the step everyone forgets

**This is the single most commonly missed deliverable in an LSC mobile story.**

The iPad app does not read org metadata live. It works from a **generated
metadata cache**. Per [Mobile App Configuration for Visit Management](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_db_schema_metadata_cache.htm&type=5):

1. **Create an object metadata cache configuration** for every object the mobile
   app must see. Configuration type is typically `Data`.
2. **Select "Web-to-Mobile Sync"** on objects whose web-side changes must reach
   the device (e.g. `ProviderSampleLimit`, `ProviderSampleLimitTemplate`,
   `ProviderSmplLmtTmplAssignment`, `ProductBatchItem`,
   `TerritoryProdtQtyAllocation`).
3. **Specify a SOQL Filter Condition** to limit what downloads to the device —
   this is a performance and data-volume control, not an optional nicety.
4. **Set the attachment download method** where relevant (e.g. on `Visit`, if a
   related list is configured, set it to `Cache`).
5. **Generate the metadata cache.** Salesforce flags this as *Important*: without
   it the app will not pick up schema changes.

### Consequences for story authoring

> **Any story that adds or changes an object, field, page layout, related list,
> or action, and targets the iPad surface, MUST carry a metadata-cache task in
> Technical Implementation and a verification item in Definition of Done.**

A Pattern B field-creation AC that ships without the cache regeneration produces
a field the rep will never see. That is a silent failure — the deploy succeeds,
the web UI shows the field, and the iPad does not.

**Mobile Sync Settings** additionally allow periodic background synchronization
during idle time to keep rep data current — mention when a story depends on data
freshness.

---

## Device Sync object model (offline transaction pipeline)

Verified against the **Agentforce Life Sciences Developer Guide** (Summer '26 /
**API v67.0**). All objects are **available in API version 65.0 and later**.

When a rep acts offline, the app records the work locally and replays it as
**device sync transactions** when connectivity returns. These objects are the
audit trail — and the place a "why did my visit not save?" defect gets diagnosed.

### `DeviceSyncTransaction` — a set of related data items to sync

The unit of offline work. Key fields for story authoring:

| Field | Notes |
|---|---|
| `OfflineUniqueIdentifier` | **Required**, idLookup. The device-side identity used for idempotent replay |
| `OfflineTimestamp` | **Required**. When the action actually happened on the device — *not* when it synced |
| `Status` | Restricted picklist: `New`, `Waiting`, `InProgress`, `Success`, `Failed`, `Retry`, `Canceled`, `Manual` |
| `DevicePlatform` | Restricted picklist: `iOS`, `Android`, `MacOS`, `Windows` |
| `DeviceType` | e.g. `Phone`, `Tablet` |
| `DependentOfflineIdentifiers` | Comma-separated dependent transaction IDs, **processed in listed order** |
| `Sequence` | Order position relative to other transactions |
| `IsBulk` | Bulk-sync only when there are **no dependencies** between transactions |
| `IsRealTime` | Eligible for real-time batch processing |
| `IsRetry`, `NumberOfFailedAttempts` | Retry semantics |
| `IsWithSignedItem` | Transaction includes a **signature** data item |
| `IsOwnerPermissionEnforced` | Respect the record owner's permissions during sync |
| `IsSimulatable`, `CanCancDpndBeRetired` | Calculated; drive the admin retry/simulate actions |
| `ExpectedRecordCount` / `ActualRecordsCount` / `TotSyncTranRecordCount` | Reconciliation counts |
| `LastRunLogId` | Lookup to `DeviceSyncTransactionLog`; empty when no errors |
| `MetadataVersion`, `AppVersion` | Version pinning — a stale device metadata version is a common failure cause |

### `DeviceSyncTransactionRecord` — a single data item to sync

Master-detail child of `DeviceSyncTransaction`.

| Field | Notes |
|---|---|
| `ObjectName` | **Required**. The object type being synced |
| `OperationType` | **Required** restricted picklist: `insert`, `update`, `delete` |
| `OfflineUniqueIdentifier`, `OfflineCreatedDate` | **Required**. Device-side identity + creation time |
| `FieldValues` | The payload. **Empty** for attachments and deletes |
| `RecordIdentifier` | Custom ID for a new record, standard ID for an existing one |
| `ProcessedRecordIdentifier` | The resulting Salesforce record ID after sync |
| `RelatedRecordId` | Lookup — refers to `Account` |
| `Sequence` | Preserves item order within the transaction |
| `Status` | Restricted picklist: `Preparing`, `Ready` |

### `DeviceSyncTransactionLog` — error/diagnostic log

Master-detail child of `DeviceSyncTransaction`; carries
`DeviceGenRecordIdentifier` to tie a log line back to a device record.

### `DeviceSyncSummary` — per-sync telemetry

The health record for a sync run. Useful for monitoring and for
"sync performance" stories.

> Field list re-verified **2026-09-10** against the
> [DeviceSyncSummary object reference](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/sforce_api_objects_devicesyncsummary.htm)
> (available API v65.0+). Two corrections were applied: the download-duration
> field is **`DataDownloadDuration`**, and the metadata-download fields plus two
> `SyncTrigger` values were missing.

| Field group | Fields |
|---|---|
| Identity | `DeviceIdentifier`, `AppVersion`, `BundleIdentifier`, `IosVersion`, `MetadataVersion` |
| Download | `DownloadStart`, `DownloadEnd`, **`DataDownloadDuration`** (calculated, ms — *not* `DownloadDuration`), `DownloadedRecords`, `DownloadCreatedRecords`, `DownloadUpdatedRecords`, `IsDownloadCompleted`, `DownloadFreezeTime` |
| Metadata download | `MetadataDownloadStart`, `MetadataDownloadDuration` (ms), `MetadataUpdated`, `MetadataVersion` |
| Upload | `UploadStart`, `UploadEnd`, `UploadDuration` (calculated, ms), `UploadRecords`, `IsUploadCompleted`, `UploadFreezeTime`, `LastSuccessfulUploadTime` |
| Offline provenance | `OfflineCreatedDate`, `OfflineLastModifiedDate`, `LastSyncTime` |
| Environment | `Network`, `SignalStrength`, `UserLocation` (geo) |
| Status | `SyncStatus` (`New`, `Pending`, `Ok`, `Error`), `ErrorCode`, `ErrorDetail`, `SyncErrorMessage` |
| Trigger | `SyncTrigger`: `Initial`, `Manual`, `Forced`, `Pin`, `Territory Switch`, `Days Offline Limit`, `Metadata In Background`, `Idle Background Sync`, `InitiatedByAIAgent` |
| Type | `Type`: `data`, `clm` |
| Misc | `S3Bucket`, `SyncSummaryData` (JSON), `FileReferenceId` → `PresentationFileReference` |

`SyncTrigger` is worth reading closely — **`Days Offline Limit`** and
**`Territory Switch`** are real business events an AC may need to cover
(a rep offline too long is forced to sync; a territory realignment forces a
re-download).

### `LifeScienceMobileApp` — device registration

Master-detail to **`UserDevice`**. One record per user device.

`ApplicationVersion`, `DeviceMetadataVersion`, `IsFullSyncEnforced`,
`IsDownloadSyncSuccessful`, `IsUploadSyncSuccessful`, `LastDownloadSyncDate`,
`LastUploadSyncDate`, `DeviceLastLocation`.

`IsFullSyncEnforced` is the admin lever to force a full resync on a device.

### `LifeSciMobileMetadataRecord` — the generated metadata cache

The cache artifact itself.

| Field | Notes |
|---|---|
| `Status` | `New`, `Queued`, `Loading`, `InProgress`, `Processing`, `Validating`, `Validated`, `Published`, `Active`, `Inactive` |
| `IntegrationStatus` | `New`, `Pending`, `Ok`, `Error` (default `New`) |
| `ProfileId` | Lookup to **`Profile`** — the cache is **profile-scoped** |
| `ParentMobileMetadataRecId` | Self-referencing hierarchy |
| `MetadataDocumentId` | Lookup to `ContentDocument` — the cache payload |
| `ApplicationVersionName` / `ApplicationVersionNumber` | App version targeting |
| `UpdateDueDate`, `UpdateAvailableAlertDate` | Cache refresh governance |
| `ErrorLog`, `IntegrationErrorCode`, `IntegrationErrorMessage` | Failure diagnostics |
| `SourceSystemName`, `SourceSystemIdentifier` | Provenance |

**`ProfileId` matters:** the metadata cache is generated per profile. A story
that adds a field for one persona must regenerate the cache for **that persona's
profile**, or that persona alone won't see it.

---

## Offline authoring rules (how offline changes an AC)

Offline is not a footnote on a happy-path AC. It changes what "Then" means,
because the outcome is **deferred** and can **fail after the user has walked
away**.

1. **Split the moment of action from the moment of persistence.** Offline, the
   rep's action succeeds locally and the server write happens later. An AC that
   says "Then the sample transaction is created" is ambiguous — say what the rep
   sees *on device* and, separately, what exists *in Salesforce after sync*.
2. **Never write a server-side error into an offline user-facing AC.** The rep
   is not connected; they cannot see a callout failure. Route sync failures to
   the admin surface (`DeviceSyncTransaction.Status = Failed` +
   `DeviceSyncTransactionLog`). This mirrors the Concur rule that integration
   errors are not shown to field users.
3. **Validation must be local to be enforceable offline.** A validation that
   needs a live query (real-time inventory, licence lookup against an external
   system) **cannot** run offline. Either the data is primed into the cache, or
   the rule degrades. Say which, explicitly.
4. **Say what is primed.** If an AC's Given depends on data being available
   offline, that data must be in the metadata cache with a SOQL filter that
   includes it. Cross-reference the cache configuration.
5. **Cover the ordering case.** Where one offline record depends on another
   (visit → sample drop → signature), the dependency is carried by
   `DependentOfflineIdentifiers` and `Sequence`. An AC should state the required
   order and what happens if a parent transaction fails.
6. **Cover conflict.** Two surfaces can touch one record. State who wins when a
   record changed on the web while the rep held an offline edit.
7. **Signature is an offline artifact.** `IsWithSignedItem` exists because
   signatures ride the offline pipeline. Sample-drop signature ACs are offline
   ACs.

### Pattern F

The AC shape for all of the above lives in `ac-pattern-library.md` as
**Pattern F — Offline / Sync Behaviour**. Use it whenever Surface is
*iPad (online + offline)* or *Both*.

---

## Per-surface behaviour matrix

Where behaviour differs by surface, put it in a matrix rather than prose — the
`concur-integration.md` precedent. Include this table in a story whenever
Surface = *Both*.

| Capability | iPad (offline) | iPad (online) | Lightning web |
|---|---|---|---|
| *e.g. Create expense* | Yes | Yes | Yes |
| *e.g. Attach receipt* | 1 attachment, new expense only | 1 attachment, new expense only | 1+ on existing |
| *e.g. Delete expense report* | No | No | Yes |

Known real examples from `concur-integration.md`: expense report **deletion** is
web-only; adding **multiple attachments to an existing expense** is web-only;
iPad allows **one** attachment on a newly created expense and cannot attach to an
existing one; attachments are ≤ **1 MB**, `PNG`/`JPG`/`JPEG`/`PDF`.

---

## Build technology on mobile

The build-technology decision (RULE 7a) is **constrained by surface**. See the
mobile column in `lsc-components.md`.

Key points:

- The LSC Mobile app's documented extension model is **Flows, Apex, and open
  APIs** — that is what Salesforce names in the app's own positioning. Prefer
  **Screen Flow + Apex + LWC** for mobile-targeted work.
- **Dynamic Actions are mobile-aware.** Per [Add Actions with Dynamic Actions](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_add_actions_with_dynamic_actions.htm),
  actions are surfaced so users "see only the actions that are relevant to the
  current visit status **and device**," and the toggle lives at **Admin Console →
  Mobile → Application Settings → Enable Dynamic Actions**. Device-conditional
  visibility is a first-class, declarative capability — use it rather than
  building two pages.
- **Do not assume OmniStudio runs in the LSC Mobile app.** OmniStudio is
  supported *in LSC*, but Salesforce's mobile-app material does not name
  OmniScript as a mobile extension path. Before proposing OmniScript for an
  iPad-targeted story, **verify** mobile support and record the result in the
  Clarification Questions table. Never assume "OmniScript handles offline
  capture" — that was a v1.9 assumption this reference exists to correct.
- **Custom LWC inline on a mobile record page** reportedly requires an
  **`lscMobileInline_` API-name prefix** for the mobile framework to render it
  inline. ⚠️ **Unverified against Salesforce Help** — the available sourcing is
  Agentforce Life Sciences Consultant (ALS-Con-201) certification material that
  cites Salesforce Help rather than Help itself. **Confirm before relying on it**,
  and mark it *(to verify)* in any story that proposes an inline mobile LWC.

---

## Personas and their primary surface

| Persona | Primary surface | Note |
|---|---|---|
| **Field Sales Representative** | **iPad (offline)** | Almost never at a desk. Assume iPad. |
| **Medical Science Liaison (MSL)** | **iPad (offline)** | Field-based scientific engagement. |
| **Key Account Manager (KAM)** | **iPad**, some web | Account planning may be web. |
| **District Sales Manager** | **iPad**, some web | Coaching in field; reporting on web. |
| **Event Organizer** | **iPad + web** | Offline Mobile is the primary surface for Events (per `concur-integration.md`). |
| **Commercial Operations Analyst** | **Lightning web** | Territory/cycle-plan design is a desk activity. |
| **Market Access Manager** | **Lightning web** | Payer/contract work. |
| **Compliance Specialist** | **Lightning web** | Oversight and reporting. |
| **LSC Admin / MuleSoft Admin** | **Lightning web** | Setup, Admin Console, integration config. |

Migrating from Veeva sharpens this: Veeva field users are **iPad-native**. A
migration story that lands a rep capability on web only is a UAT failure, not a
scope reduction. See `veeva-to-lsc-mapping.md`.

---

## Definition-of-Done additions for mobile stories

Add these to the story's Definition of done whenever Surface includes iPad:

- [ ] Behaviour verified **in the Life Sciences Cloud Mobile app on iPad**, not only in Lightning web
- [ ] Object metadata cache configuration created/updated for every new or changed object (with SOQL Filter Condition set)
- [ ] **Metadata cache regenerated** and the change confirmed visible on a device for **each affected profile**
- [ ] `Web-to-Mobile Sync` selected where web-side edits must reach the device
- [ ] Offline path verified: action performed with connectivity disabled, then synced, and the resulting records confirmed
- [ ] Sync failure path verified: `DeviceSyncTransaction.Status = Failed` with a diagnostic `DeviceSyncTransactionLog` entry, and no end-user error shown to the rep
- [ ] Touch targets and layout verified in both iPad **landscape and portrait**

---

## Clarification questions to ask

Add to the Clarification Questions table when surface is in play:

| # | Question | Impact | Owner |
|---|----------|--------|-------|
| 1 | Which surface(s) must this run on — LSC Mobile iPad app, Lightning web, or both? | Determines build technology and whether offline rules apply | Product |
| 2 | Must this work with **no connectivity**, or is online-only acceptable? | Drives metadata cache priming and Pattern F ACs | Product / Commercial Ops |
| 3 | Which profiles need the regenerated metadata cache? | Cache is profile-scoped; a missed profile means an invisible feature | Technical |
| 4 | What data must be primed offline, and what SOQL filter bounds it? | Device data volume and offline validation feasibility | Technical |
| 5 | On a web-vs-offline conflict on the same record, which wins? | Conflict resolution AC | Commercial Ops |
| 6 | Is OmniStudio confirmed supported on the LSC Mobile app for this interaction? | If not, the build technology must be Flow/Apex/LWC | Technical |

---

## Verified references

Primary sources, checked Aug 2026. The `salesforce-docs` MCP was in an error
state during this revision, so `developer.salesforce.com` and
`help.salesforce.com` were used directly.

- [Agentforce Life Sciences Developer Guide — overview](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_cloud_overview.htm) — confirms the rename to Agentforce Life Sciences
- [Mobile Sync data model](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_mobile_sync.htm) — Device Sync objects
- [Mobile Metadata data model](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_mobile_metadata.htm) — metadata cache model
- [`LifeScienceMobileApp` object reference](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/sforce_api_objects_lifesciencemobileapp.htm)
- [Mobile App Configuration for Visit Management](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_db_schema_metadata_cache.htm&type=5) — object metadata cache, Web-to-Mobile Sync, SOQL Filter Condition, attachment download method, generate cache
- [Add Actions with Dynamic Actions](https://help.salesforce.com/s/articleView?id=ind.lsc_visit_management_add_actions_with_dynamic_actions.htm) — device-aware actions; Admin Console → Mobile → Application Settings
- [Life Sciences Cloud Mobile — App Store](https://apps.apple.com/us/app/life-sciences-cloud-mobile/id6499238627) — iPadOS requirement, offline positioning, Flows/Apex extensibility
- [LSC for Customer Engagement product page](https://www.salesforce.com/life-sciences/cloud/customer-engagement/) — "Offline-enabled iPad App"; GA October 2025
- Object field detail: **Agentforce Life Sciences Developer Guide, Summer '26 (API v67.0)** — `DeviceSyncSummary`, `DeviceSyncTransaction`, `DeviceSyncTransactionRecord`, `DeviceSyncTransactionLog`, `LifeScienceMobileApp`, `LifeSciMobileMetadataRecord`

> ⚠️ **Open verification item:** the `lscMobileInline_` LWC prefix (see *Build
> technology on mobile*). Sourced only from certification-prep material citing
> Salesforce Help. Confirm against Help before treating it as a naming rule.
