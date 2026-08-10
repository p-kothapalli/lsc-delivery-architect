# LSC Standard Object Catalog — Complete (Summer '26 / API v67.0)

**Authoritative, verified list of every Life Sciences Cloud standard object.**
Fetched verbatim from the official
[Life Sciences Cloud Developer Guide → Standard Objects](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_sforce_api_objects.htm)
(Summer '26, **API version 67.0** — the "Latest" release at capture time).

> **How to use this file.** `lsc-object-model.md` is the *curated, business-term*
> starting point for writing stories. **This file is the complete, ground-truth
> object catalog** — use it to (a) confirm an LSC object actually exists and get
> its exact API name, and (b) find the right object for a capability. Object
> availability is version-gated; the **"Since"** column is the API version an
> object was introduced (blank = pre-v61 / long-standing). **Field-level detail
> is NOT in the dev guide list** — to get every field, run a `describe` against
> an org where LSC is enabled, inspect the WSDL, or use a schema viewer.
>
> **This workspace (IBXQA) is a PNM org**, so most of these objects are **not
> deployed here**. Treat any object you cannot verify via `code-review-graph` /
> a `describe` as *proposed / to-be-provisioned* in a Clarification Question —
> do not assert it exists in the target org (SKILL RULE 3a).

LSC groups these into four engagement data models — **Clinical Engagement**,
**Customer Engagement** (commercial), **Patient Engagement**, and **MedTech
Commercial Engagement** — plus shared platform objects. The catalog below is
organized by **functional cluster** (more actionable for story writing than the
four top-level models); the commercial/medical/market-access clusters most LSC
stories touch are listed first.

---

## Commercial — Visits / Calls

| Object | Purpose | Since |
|---|---|---|
| **Visit** | Track a field rep's visit to a health care provider. | |
| **ProviderVisit** | Details of a field user's visit to an HCP (e.g. a rep discussing product usage/efficacy). | 65.0 |
| **ProviderVisitChangedEvent** | Change event for a data-manipulation operation on a provider visit. | 65.0 |
| **ProviderVisitProdDetailing** | Products detailed during a visit (brand, therapeutic area, etc.). | 65.0 |
| **ProviderVisitProdDiscussion** | Additional notes about products discussed during a visit. | 65.0 |
| **ProviderVisitDtlProductMsg** | Delivered messages and HCP reactions for products discussed in a visit. | 65.0 |
| **ProviderVisitMarketingItem** | Marketing items provided to the HCP as part of a visit. | 65.0 |
| **ProviderVisitRqstSample** | Sample products requested to be shipped to the HCP during a visit. | 65.0 |
| **VisitedParty** | The contact person at the account being visited. | 49.0 |
| **Visitor** | The sales reps performing visits. | |
| **ProductRequired** | A product needed to complete a visit. | |
| **PrvdEngmtComplianceCycle** | Duration/progress of provider compliance cycles. | |

## Commercial — Sample Management & Inventory

| Object | Purpose | Since |
|---|---|---|
| **ProductionBatch** | A batch of homogeneous products from the same production line. | 65.0 |
| **ProductBatchItem** | Details about product items in each batch. | 65.0 |
| **ProductItem** | Stock of a particular product at a particular location (field service inventory unit). | |
| **ProductItemTransaction** | An action taken on a product item (LSC-extended). | 65.0 |
| **ProductTransfer** | Transfer of inventory between locations (LSC-extended). | 65.0 |
| **ProductDisbursement** | Details about the product being disbursed. | 65.0 |
| **ProductRequest** | A device/sample-order request (LSC-extended for sample orders). | 65.0 (Samples) |
| **ProductRequestLineItem** | Junction between ProductRequest and ProductTransfer. | 50.0 / 65.0 (Samples) |
| **ProductFulfillmentLocation** | Associates a business account + product inventory with the responsible rep. | 49.0 |
| **ProductAvailabilityProjection** | Projected product quantity available at a location over time (Intelligent Sales). | 55.0 |
| **InventoryCountAssessment** | An inventory count performed at a location. | 65.0 |
| **InventoryCntProdtBatchItem** | Inventory count of a product batch at a location (child of the count assessment). | 65.0 |
| **InventoryOperation** | Operations on inventory — transfers, disbursements, adjustments. | 65.0 |
| **SerializedProduct** | Serial numbers for each individual product in inventory. | 50.0 |
| **ProviderSampleLimit** | Sample limits + remaining quantity for an account/product. | 65.0 |
| **ProviderSampleLimitTemplate** | Definition/rules of sample-limit templates. | 65.0 |
| **ProviderSmplLmtTmplAssignment** | Junction relating sample-limit templates to products. | 65.0 |
| **PrvdVstSmplLmtTransaction** | Samples / sample-shipment requests captured in a visit. | 65.0 |
| **PrvdVstSmplLmtDiscrepancy** | Discrepancies when samples/requests exceed a sample limit. | 65.0 |
| **LifeSciProductAcctRstrc** | Product use limitations for an account (detailing/sampling compliance). | 65.0 |
| **UnitOfMeasure** | Units of measure for care metrics/observations. | 49.0 |

## Commercial — Products & Pricing

| Object | Purpose | Since |
|---|---|---|
| **Product2** | A product your org sells. | |
| **Pricebook2** | A price book (list of products your org sells). | |
| **Pricebookentry** | A product entry (price book ↔ product association). | |
| **LifeSciMarketableProduct** | All products a company manufactures/markets/sells/competes with (brands, indications, therapeutic areas; sampled/ordered/promo items). | 65.0 |
| **LifeSciMktProdtCodeSet** | Relationship between a marketable product and a code set for a jurisdiction. | 65.0 |
| **ProductGuidance** | Key product messages/objectives that guide users working with a product. | 65.0 |

## Commercial — Territory Management, Alignment & Scoring

| Object | Purpose | Since |
|---|---|---|
| **TerrGeoAssignmentRule** | Alignment rules assigning accounts to territories by geocode. | 65.0 |
| **TerrProvAffilAssignRule** | Rule for aligning affiliated accounts by role/specialty/account type. | 65.0 |
| **TerritoryAccountScore** | Intelligent provider scores to surface top accounts in a territory. | 65.0 |
| **TerritoryAcctProdMsgScore** | Intelligent product-message score for territory accounts. | 65.0 |
| **TerritoryAcctRcmdAction** | Recommended engagement actions for an account at territory level. | 65.0 |
| **TerritoryBusinessPlan** | Strategic outline to manage/expand customer relationships in a territory. | 65.0 |
| **TerritoryContentTmplAsgnt** | Links a territory to a content template. | 65.0 |
| **TerritoryProdtQtyAllocation** | Product quantity allocation to a territory (validated vs. remaining/max limits). | 65.0 |
| **TerritoryUserDowntime** | Blocks of time when reps are out of their territories. | 65.0 |
| **ProviderAcctTerritoryInfo** | Engagement data between an account and a user in a territory (next visit, preferred address, planned activities). | 65.0 |
| **ProviderAcctProductInfo** | HCP/HCO info at territory + product level (segmentation, rankings). | 65.0 |
| **PrvdAccountTerritorySummary** | Summaries for a provider account across aligned territories. | 65.0 |
| **PrvdAccountUserGroupInfo** | Classification values for the provider account user group. | 65.0 |
| **ProductTerritoryAvailability** | Products aligned to territories. | 65.0 |
| **ProductTerrDtlAvailability** | Extension/detail of ProductTerritoryAvailability (internal). | 65.0 |
| **ServiceTerritoryRelationship** | Relationship between service territories by work types performed. | 56.0 |

## Commercial — Activity Planning, Goals & Cycle Plans

| Object | Purpose | Since |
|---|---|---|
| **ActivityPlan** | A user's activity goals for the cycle. | 65.0 |
| **ActivityPlanTerritory** | Territory details associated with an activity plan. | 65.0 |
| **ActivityTiming** | An activity repeated at regular intervals over a period. | 52.0 |
| **ProviderActivityGoal** | Goals for provider accounts. | 65.0 |
| **ProviderActivityGoalLimit** | Limits defined for provider activity goals. | 67.0 |
| **ProviderActivityGoalMeasure** | Goal measurement for an activity type. | 65.0 |
| **ProviderActivityMeasureType** | Details of the activity-goal measure type. | 65.0 |
| **ProviderActvtyPlanAdjusment** | Adjustment requests for an activity plan. | 65.0 |
| **PrvdActvtyGoalMeasureProdt** | Products associated with the activity-goal measure. | 65.0 |
| **PrvdActvtyPlanAdjProdt** | Products associated with a provider activity-plan adjustment. | 65.0 |

## Commercial — Account Lists, Actionable Lists & Segmentation

| Object | Purpose | Since |
|---|---|---|
| **ActionableList** | An actionable list. | 65.0 |
| **ActionableListFilterCriteria** | Logical expression of filter conditions for an actionable list's dataset. | 65.0 |
| **LifeScienceAccountList** | Type of account list — filter, static list, routine. | 65.0 |
| **LifeScienceAccountListObject** | Object referenced in the provider account list. | 65.0 |
| **LifeSciAccountListColumn** | Columns selected from accounts/related objects in account filters. | 65.0 |
| **LifeSciAccountListMember** | Account static-list and routine membership. | 65.0 |
| **LifeSciAcctGrpAssignment** | Junction between an account and an actionable list. | 65.0 |
| **LifeSciAcctListFilterCrit** | Rules/conditions from Account (or related objects) to filter LSC accounts. | 65.0 |

## Key Account Management (KAM) — Account Plans & Sprints

| Object | Purpose | Since |
|---|---|---|
| **AccountPlanParticipant** | Team members participating in the account plan. | 65.0 |
| **AccountPlanProduct** | Products associated with an account plan/its objectives. | 65.0 |
| **AccountPlanRelationship** | Relationship between multiple account plans for KAM. | 65.0 |
| **AccountPlanRelaObjAnalysis** | Strategic analysis of objects related to the account plan. | 65.0 |
| **AccountPlanStakeholder** | Key individuals who influence an account or have a vested interest. | 65.0 |
| **AccountPlanStkhldrAction** | Junction — an action for an account plan tied to a stakeholder. | 65.0 |
| **AccountPlanStkhldrProduct** | Junction — products associated with a stakeholder for an account plan. | 65.0 |
| **AcctPlanPtcpStakeholder** | Junction — account-plan participant ↔ stakeholder collaboration. | 65.0 |
| **ActionPlan** | Instance of the compliance program assigned to an account (LSC-extended). | 65.0 (LSC) |
| **ActionPlanItem** | Junction between Action Plan and Provider Engagement Compliance Cycle. | 65.0 (LSC) |
| **ActionPlanStatusPeriod** | Historical status changes of an action plan. | |
| **ActionPlanTemplate** | Instance of an action-plan template. | 65.0 (LSC) |
| **ActionPlanTemplateVersion** | A version of an action-plan template. | |
| **ActionPlanTemplateAssignment** | Association of a template with a care-plan template/goal/problem definition. | |
| **ActionPlanTemplateItem** | Instance of an item on a template version (KAM). | 64.0 (KAM) |
| **ActionPlanTemplateItemValue** | Value associated with an action-plan template item. | |
| **Sprint** | A timeframe within which account action plans are executed (KAM). | 65.0 |
| **GoalDefinition** | A reusable goal/business objective; instantiates GoalAssignment records. | |
| **GoalDefinitionProduct** | Junction — goal definition ↔ product (objective for a product). | 65.0 |
| **GoalAssignment** | Goals that are part of a care plan. | |

## Managed Events / Event Management

| Object | Purpose | Since |
|---|---|---|
| **MngEvent** | Details of a managed event. | 67.0 |
| **MngEventType** | A type of managed event. | 67.0 |
| **MngEventParticipant** | A managed-event participant and their participation details. | 67.0 |
| **MngEventParticipantDiscrepancy** | Discrepancies where participants don't meet event limits/restrictions. | 67.0 |
| **MngEventProduct** | Junction — managed event ↔ focus-area product. | 67.0 |
| **MngEventResource** | A resource required for a managed event. | 67.0 |
| **MngEventResourcePreference** | Preference rank of a requested managed-event resource. | 67.0 |
| **MngEventTerritory** | Junction — managed event ↔ territory. | 67.0 |
| **MngEventBudget** | Junction — managed event ↔ allocated budget. | 67.0 |
| **EventPlan** | The plan for an event type. | 67.0 |
| **EventPlanItem** | An item of an event plan. | |
| **EventPlanBudget** | Junction — event plan ↔ allocated budget. | 67.0 |
| **EventPlanParticipant** | Junction — event plan ↔ participant. | 67.0 |
| **EventPlanProduct** | Junction — event plan ↔ product/category. | 67.0 |
| **EventPlanSubject** | Junction — event plan ↔ subject. | 67.0 |
| **EventPlanSvcSpclzn** | Junction — event plan ↔ event service specialization (compliance/budget rules). | 67.0 |
| **EventPlanTerritory** | Junction — event plan ↔ territory. | 67.0 |
| **EventMgmtParticipantType** | Category/classification of participants for a managed event. | 67.0 |
| **EventMgmtParticipantRole** | Role a participant performs (organize/coordinate/present/attend). | 67.0 |
| **EventMgmtPtcpTypeRoleMap** | Maps allowed participant roles to participant types per event type. | 67.0 |
| **Expert** | An expert who can speak/present at managed events. | 67.0 |
| **ExpertSubject** | Junction — expert ↔ subject they're certified to present. | 67.0 |
| **Subject** | A subject discussed/presented at managed events. | 67.0 |
| **SubjectAssignment** | Junction — subject ↔ managed event. | 67.0 |
| **SubjectProduct** | Junction — managed-event subject ↔ product. | 67.0 |
| **SubjectMaterialTemplate** | Subject material template approved for managed events. | 67.0 |
| **RestrictedParty** | A party (participant/speaker/vendor) restricted from an event. | 67.0 |
| **BudgetMngEventType** | Junction — budget ↔ permitted event types. | 67.0 |
| **BudgetProduct** | Junction — budget ↔ product it's assigned to. | 67.0 |
| **BudgetTerritory** | Junction — budget ↔ territory it's assigned to. | 67.0 |

## Expenses — SAP Concur Integration

> Full sync model, statuses, and rules are in `concur-integration.md`.

| Object | Purpose | Since |
|---|---|---|
| **Expense** | An expense related to a visit (LSC-extended standard Expense). | 65.0 |
| **ExpenseType** | Category used to classify an expense. | 65.0 |
| **ExpenseParticipant** | Junction — expense ↔ the person who incurred it. | 67.0 |
| **EstimatedExpense** | Estimated expense of a managed event. | 67.0 |
| **EstimatedExpensePtcpAlloc** | Allocation of a managed-event participant to an estimated expense. | 67.0 |
| **IntegrationJobRun** | Statistical details of asynchronous integration (sync) jobs. | 65.0 |

## Medical / MSL — Insights & Inquiries

| Object | Purpose | Since |
|---|---|---|
| **MedicalInsight** | Key information observed/heard (meetings, calls, research) to inform patient-care strategy. | |
| **MedicalInsightAccount** | The account that provided the medical insight. | |
| **MedicalInsightProduct** | The product related to the medical insight. | |
| **MedicalInsightGoalDef** | The goal needed to address the medical insight. | |
| **CustomObjectParticipant** | Individual collaborating on / to be informed of the Medical Insight (LSC-extended). | |
| **UserReaction** | User reactions (upvote/downvote) to a medical insight (trending). | |
| **Inquiry** | An inquiry logged by a sales rep or other user. | 65.0 |
| **InquiryQuestion** | A question asked by an HCP during an inquiry. | 65.0 |
| **InquiryQuestionAnswer** | The MSL's answer to an inquiry question. | 65.0 |
| **PartyPublication** | Details of a party's publication. | |

## Content — Presentations / CLM / Approved Email / Documents

| Object | Purpose | Since |
|---|---|---|
| **Presentation** | A collection of presentations (activation dates, emailable, tags, gestures). | 65.0 |
| **PresentationPage** | Reusable pages usable within a presentation (each may contain multiple slides). | 65.0 |
| **PresentationLinkedPage** | Connection between a presentation and its pages. | 65.0 |
| **PresentationPageProduct** | Link between a presentation page and a product (and product message). | 65.0 |
| **PresentationForum** | Forums (call/meeting/order) where the presentation was shown. | 65.0 |
| **PresentationClickStrmEntry** | Clickstream data captured while a presentation is shown. | 65.0 |
| **PresentationPartyAccess** | Access-sharing of a presentation with an HCP (with expiration). | 65.0 |
| **PresentationContent** | AI-generated static asset at run-time from a content definition. | 66.0 |
| **PrstContentDefinition** | Reusable config to generate an end-user content asset (e.g. audio summary). | 66.0 |
| **PrstCntntDefAssignment** | Assigns a content definition (podcast/text summary) to users/profiles/groups. | 66.0 |
| **PrstCntntUsageSummary** | Usage of a content asset (times consumed, progress). | 66.0 |
| **LifeSciEmailTemplate** | Pre-designed, approved email templates sent to HCPs. | 65.0 |
| **LifeSciEmailTmplFragment** | Reusable components inserted into email templates. | 65.0 |
| **LifeSciEmailTmplRelaFrgmt** | Connectors linking email templates and fragments. | 65.0 |
| **LifeSciEmailTmplSnapshot** | Versions of an email template for tracking. | 65.0 |
| **LifeScienceEmail** | Sendable messages — content, send status, responses. | 65.0 |
| **LifeScienceDocument** | A signed document + document fields. | |
| **LifeScienceDocumentTemplate** | Template name + general info about a template. | |
| **LifeSciDocTemplateVersion** | Version-specific template info. | |
| **DocumentTemplate** | Dynamic document generation. | 56.0 |

## Digital Signature, Verification & Compliance

| Object | Purpose | Since |
|---|---|---|
| **DigitalSignature** | A signature (LSC-extended). | 65.0 |
| **DigitalSignatureRequest** | Reserved for future use. | |
| **DigitalVerification** | Verification of a related record. | 60.0 |
| **DigitalVerificationSetup** | A verification setup (number of signatures, related record action). | 60.0 |
| **DigitalVerfSetupDetail** | Contextual details of a verification setup (verifier, messages). | 60.0 |
| **ComplianceStatementDef** | Compliance statements shown across visits/consent capture (ack required/optional/informational). | |

## Consent & Communication Subscriptions

| Object | Purpose | Since |
|---|---|---|
| **CommSubscription** | A customer's subscription preferences for a communication (LSC-extended). | 65.0 |
| **CommSubscriptionConsent** | A customer's consent to a communication subscription (LSC-extended). | 65.0 |
| **CommSubConsentCmplSnpsht** | Snapshot of compliance info captured at time of consent. | 65.0 |
| **ContactPointConsent** | Consent to be contacted via a specific contact point (LSC-extended). | 65.0 |
| **ContactPointBestContactTime** | Optimal time to visit associated contact-point addresses. | 65.0 |
| **ContactPointSocial** | Social-media identifiers/contact points for an individual/account. | 65.0 |
| **DataUsePurpose** | Reason for contacting a prospect/customer (LSC-extended). | 65.0 |

## Provider / HCP–HCO Master Data (shared with PRM)

| Object | Purpose | Since |
|---|---|---|
| **HealthcareProvider** | Business-level details about the healthcare org or practitioner. | |
| **HealthcareProviderNpi** | National Provider Identifier(s) for facilities/practitioners (US). | |
| **HealthcareProviderService** | Junction — HealthcareService ↔ provider/facility/practitioner-facility. | 59.0 |
| **HealthcareProviderSpecialty** | Specialties for a practitioner or service-provider org. | |
| **HealthcareProviderTaxonomy** | Taxonomy/subspecialty codes for a practitioner/facility. | |
| **HealthcareFacility** | A healthcare facility and its physical/functional/geographic/business details. | 51.0 |
| **HealthcareFacilityNetwork** | Junction — the insurance network a location/entity is part of. | |
| **HealthcarePayerNetwork** | An insurance network group (e.g. an EPO plan). | |
| **HealthcarePractitionerFacility** | Locations where a practitioner provides services. | |
| **HealthcareServiceDetail** | Junction — CareService ↔ CodeSetBundle. | 59.0 |
| **CareService** | A treatment/service/procedure offered by a provider/practitioner/facility. | 59.0 |
| **CareSpecialty** | Provider specialty codes and descriptions. | |
| **CareSpecialtyTaxonomy** | Junction between CareSpecialty and CareTaxonomy. | 52.0 |
| **CareTaxonomy** | A static list of taxonomy codes. | |
| **CareProviderAdverseAction** | Adverse actions against a provider (malpractice, revoked license). | 47.0 |
| **CareProviderFacilitySpecialty** | Specialties a practitioner provides at a given location. | |
| **CareProviderSearchableField** | Denormalized PRM data queried by provider-search APIs (performance). | 47.0 |
| **CareProviderSearchConfig** | Fields that can appear in provider-search results. | 48.0 |
| **CareSiteIstgrSearchableFld** | Info about the clinical-trial investigator associated with a site. | 63.0 |
| **ProviderAffiliation** | Relationship between two HCPs/HCOs. | 65.0 |
| **ProviderAffiliationProduct** | Influence relationship between two HCPs regarding a product. | 65.0 |
| **ProviderSearchSyncLog** | Provider-search data-sync status log for an HCP record. | 49.0 |
| **HlthCareProvTreatedCondition** | Junction — provider/facility/practitioner ↔ treated problem definition. | 59.0 |
| **BoardCertification** | A practitioner's board certifications. | |
| **BusinessLicense** | Licenses of a party role (HCP or producer). | |
| **BusinessLicenseProduct** | Licenses required to be linked to a product for the HCP. | 65.0 |
| **Accreditation** | Professional accreditations of a facility. | |
| **Award** | A person's/organization's professional awards. | |
| **PersonEducation** | Professional education for a person in a provider role. | |
| **PersonEmployment** | A person's employment. | |
| **Applicant** | A care-program enrollee represented as an applicant. | 59.0 |
| **Identifier** | Identifier information for multiple objects. | 51.0 |
| **CareSystemFieldMapping** | Mapping from source-system fields to Salesforce entities/attributes. | |

## Address, Location, Alerts & General Platform

| Object | Purpose | Since |
|---|---|---|
| **Address** | A mailing, billing, or home address. | |
| **Location** | Location info incl. responsible user (LSC-extended). | 65.0 |
| **AppAlert** | An alert message at object/tab/global level. | 65.0 |
| **AppAlertTerritory** | Junction — Alert ↔ Territory where the alert is sent. | 65.0 |
| **AppAlertUserResponse** | User action for an alert. | 65.0 |
| **RecordAction** | Relationship between a record and an action (e.g. a flow). | 42.0 |
| **RecordAlert** | Alert about a specific record (status + active period). | 65.0 |
| **ClinicalAlert** | Warning/notification for healthcare entities (patient/location/provider/procedure/medication). | 51.0 |
| **AuthorNote** | Notes on records with author + authored-time. | 52.0 |
| **MergeRequest** | Tracks merge history (losing → winning records). | 65.0 |
| **Team** | A team of members associated with an organization. | 58.0 |
| **TeamMember** | A member associated with a team. | 58.0 |
| **TimePeriod** | Time period used to calculate indicator performance/result. | |
| **UserAdditionalInfo** | Additional user info (identifiers, preferences, return address). | 65.0 |

## Clinical Engagement / EHR (shared clinical model)

| Object | Purpose | Since |
|---|---|---|
| **AllergyIntolerance** | Clinical assessment of a patient's allergy/intolerance. | 51.0 |
| **CarePerformer** | The person performing care (observations, procedures, immunizations). | 51.0 |
| **ClinicalEncounter** | A patient's healthcare encounter (pre-admission → stay → discharge). | 51.0 |
| **ClinicalEncounterDiagnosis** | A diagnosis related to a clinical encounter. | 51.0 |
| **ClinicalEncounterFacility** | Facilities involved in an encounter + time spent. | 51.0 |
| **ClinicalEncounterIdentifier** | Identifier info for a clinical encounter. | 51.0 |
| **ClinicalEncounterProvider** | Providers involved in an encounter. | 51.0 |
| **ClinicalEncounterReason** | Reasons the encounter was required. | 51.0 |
| **ClinicalEncounterSvcRequest** | Service requests related to a clinical encounter. | 51.0 |
| **ClinicalServiceRequest** | Requests for a procedure/diagnostic service to plan/propose/perform. | 51.0 |
| **ClinicalServiceRequestDetail** | Associates records from various objects to a service request (multi-object junction). | 51.0 |
| **ClinicalDetectedIssue** | A detected issue from a clinical activity. | 55.0 |
| **ClinicalDetectedIssueDetail** | Additional info about a clinical detected issue. | 55.0 |
| **CodeSet** | Industry-defined codes in the context of their systems/versions. | 50.0 |
| **CodeSetBundle** | A group of code sets across systems/versions referring to the same concept. | 50.0 |
| **DiagnosticSummary** | Findings, interpretations, summaries of tests performed on patients. | 51.0 |
| **DiagnosticSummaryDetail** | Additional info for document-reference-type DiagnosticSummary records. | 52.0 |
| **HealthCondition** | A clinical condition/problem/relevant occurrence. | 51.0 |
| **HealthConditionDetail** | Associates body-site/laterality codes to HealthCondition records. | 52.0 |
| **Medication** | Detailed info about medications. | 51.0 |
| **MedicinalIngredient** | Substances/drugs used as ingredients in a medication (child of Medication). | 52.0 |
| **MedicationDispense** | Dispense of a medication to a patient + administration instructions. | 54.0 |
| **MedicationRequest** | A request/order for medication supply + administration info. | 51.0 |
| **MedicationStatement** | Medication the patient is taking or has taken. | 51.0 |
| **MedicationStatementDetail** | Additional info for MedicationStatement records. | 54.0 |
| **PatientMedicationDosage** | Dosage info for medication (used in statement/request/dispense). | 51.0 |
| **PatientMedicalProcedure** | A healthcare procedure the patient has/will undergo. | 51.0 |
| **PatientMedicalProcedureDetail** | Associates records to a procedure record (multi-object junction). | 51.0 |
| **PatientHealthReaction** | A patient's adverse reaction to an allergy/intolerance/immunization. | 51.0 |
| **PatientImmunization** | A patient's immunizations. | 51.0 |
| **PatientImmunizationProtocol** | Protocol followed for a patient's immunization (child of PatientImmunization). | 56.0 |

## Research Studies / Clinical Trials

| Object | Purpose | Since |
|---|---|---|
| **ResearchStudy** | A research study's design, execution, and oversight. | 61.0 |
| **ResearchStudyCandidate** | A research participant (account + subject status). | 61.0 |
| **ResearchStudyCmprGroup** | A research-study comparison group. | 61.0 |
| **ResearchStdyCmprGroupCndt** | Junction — control group ↔ study candidate. | 61.0 |
| **ResearchStdyCndtStatusPrd** | Duration a candidate holds a specific status. | 61.0 |
| **ResearchStudyProtocolInfo** | Research-study protocol document details. | 62.0 |
| **ResearchStudyRelation** | Related research studies. | 61.0 |
| **ResearchStdyRandomization** | Randomization-algorithm config for a study. | 61.0 |
| **RsrchStdyRandomizationBlock** | A block generated from randomization params. | 61.0 |
| **ResearchStudyRndmBlockSlot** | Individual randomization-block items for a block. | 61.0 |
| **RsrchStdyRandomizationCrit** | Criteria for grouping study candidates. | 61.0 |
| **ResearchStdySearchableField** | Common searchable dataset across objects for research studies. | 61.0 |

## Adverse Events / Pharmacovigilance

| Object | Purpose | Since |
|---|---|---|
| **AdverseEventEntry** | Event related to unintended/anticipated effects on research participants. | 61.0 |
| **AdverseEventAction** | Preventive/ameliorating actions for the adverse event. | 61.0 |
| **AdverseEventCause** | Entity suspected to have caused the adverse event. | 61.0 |
| **AdverseEventContribFactor** | Factors that increased probability/severity of the event. | 61.0 |
| **AdverseEventOutcome** | Type of outcome from the adverse event. | 61.0 |
| **AdverseEventParty** | Who/what participated in the event and how. | 61.0 |
| **AdverseEventSupportInfo** | Supporting information relevant to the event. | 61.0 |
| **AdverseEvntResultingEffect** | Effect on the subject due to this event. | 61.0 |

## Patient Engagement / Care Programs (Patient Services)

| Object | Purpose | Since |
|---|---|---|
| **CareProgram** | A set of activities (therapy, financial assistance, education, wellness) offered to participants. | |
| **CareProgramDetail** | Detail records related to the care program. | 61.0 |
| **CareProgramAssistance** | Junction between Care Program and Program objects. | 61.0 |
| **CareProgramCampaign** | Relationship between Care Program and Campaign (associate campaigns to a program). | |
| **CareProgramEligibilityRule** | Rule defining patient enrollment-eligibility criteria (CareProgram ↔ EnrollmentEligibilityCriteria). | |
| **CareProgramEnrollee** | A participant enrolled in a care program. | |
| **CareProgramEnrolleeProduct** | Affiliation of an enrollee to a program product/provider. | |
| **CareProgramEnrollmentCard** | A membership card (membership number/enrollment code). | |
| **CareProgramGoal** | A business/clinical goal related to a care program. | |
| **CareProgramProduct** | Affiliation between a program and a product/provider. | |
| **CareProgramProvider** | A business account that is the service provider for a program product. | |
| **CareProgramSite** | Details about the care-program site. | 61.0 |
| **CareProgramSiteContract** | Association of a program site and a contract. | 62.0 |
| **CareProgramStatusPeriod** | Historical status changes of a care program. | 61.0 |
| **CareProgramTeamMember** | A person delivering services under a program (manager/coordinator). | |
| **CarePgmEnrleeStatusPeriod** | Historical status/stage changes of an enrollee. | 61.0 |
| **CarePgmEnrolleeWorkOrder** | Work order executed for an enrollee. | 58.0 |
| **CarePgmEnrolleeWkOrdStep** | A step in a work order executed for an enrollee. | 58.0 |
| **CarePgmEnrollmentEvalRslt** | Result of an eligibility evaluation for a study/program. | 62.0 |
| **CarePgmProvHealthcareProvider** | Junction — primary HCP for a care-program provider. | 49.0 |
| **CarePgmTeamMbrRolePeriod** | Historical role changes of a program team member. | 61.0 |
| **Benefit** | Benefits associated with the financial-assistance program. | 51.0 |
| **BenefitType** | Type of benefit available to the enrollee. | 51.0 |
| **EnrollmentEligibilityCriteria** | Criteria defining patient eligibility for care programs. | |
| **ProgramEnrlEligibilityCrit** | Junction between Program and EnrollmentEligibilityCriteria. | 61.0 |
| **ProgramEnrollment** | Details of enrollment for benefits in a program. | 57.0 |
| **ProgramRecommendationRule** | Eligibility criteria + recommendation for a program. | 61.0 |
| **CareRegisteredDevice** | A device/registration for a patient or enrollee. | 49.0 |
| **AdvTherapyFieldOptOverride** | Fields with changed optionality based on parameters. | 59.0 |

## Care Barriers / SDOH / Determinants

| Object | Purpose | Since |
|---|---|---|
| **CareBarrier** | Circumstances/obstacles affecting a patient/member. | 45.0 |
| **CareBarrierType** | Standard defined list of barriers for an org. | 45.0 |
| **CareBarrierDeterminant** | Relationship of a barrier to a determinant. | 45.0 |
| **CareDeterminant** | Determinants of health (safe housing, employment, food access). | 45.0 |
| **CareDeterminantType** | Standard defined list of determinants (domain + type). | 45.0 |
| **CareInterventionType** | Standard defined list of interventions for an org. | 45.0 |

## Benefits / Coverage / Payer / Market Access

| Object | Purpose | Since |
|---|---|---|
| **CareBenefitVerifyRequest** | Request for verification of benefits. | 53.0 |
| **CarePreauth** | Preauthorizations for care under a member's plan. | |
| **CarePreauthItem** | Items included in a care preauthorization. | |
| **CoverageBenefit** | Benefits provided to a covered member by a purchaser's plan. | |
| **CoverageBenefitItem** | A specific service covered by the insurance plan. | 53.0 |
| **CoverageBenefitItemLimit** | Benefit details — expenditures, limits, coverage levels, eligibility, exclusion. | 53.0 |
| **Formulary** | Formulary covered by the payer's insurance plan. | 65.0 |
| **FormularyItem** | Products in the formulary (drug tier, coverage, copay). | 65.0 |
| **Member** | A person covered under the insurance plan. | |
| **MemberPlan** | Insurance coverage details for a member/subscriber. | |
| **Payer** | A health-insurance company (Account record). | |
| **PlanBenefit** | Standard benefits available under a plan. | |
| **PlanBenefitItem** | Details of a benefit under a purchaser's plan. | |
| **Purchaser** | The organization (employer) providing insurance plans for members. | |
| **Purchaser Payer Association** | Records purchasers who buy plans from payers (AccountAccountRelation). | |
| **PurchaserPlan** | A payer plan a purchaser makes available to members. | |
| **PurchaserPlanAssn** | Junction — purchaser ↔ plans offered to members. | |

## Assessments / Discovery Framework & Surveys

| Object | Purpose | Since |
|---|---|---|
| **AssessmentTask** | Activities (registration, order authorization) to capture information. | |
| **AssessmentEnvelope** | An envelope containing assessments related to a user. | 58.0 |
| **AssessmentEnvelopeItem** | An item in an assessment envelope. | 58.0 |
| **SurveyResponse** | A participant's response to a survey (LSC-extended). | |
| **SurveyResponseOffline** | Offline survey response (status, location, completion time). | 65.0 |
| **SurveyQstnResponseOffline** | A participant's answer to a survey question (offline/staging). | 65.0 |

## Custody Chain (Serialization / Cold Chain)

| Object | Purpose | Since |
|---|---|---|
| **CustodyChainEntry** | An entry/event in the chain of custody. | 59.0 |
| **CustodyItem** | An item in the custody chain. | 59.0 |
| **CustodyVerfcTypeOverride** | Verification of an entry in the chain of custody. | 59.0 |

## Indicators & Outcomes (Value / Outcome Management)

| Object | Purpose | Since |
|---|---|---|
| **IndicatorDefinition** | The indicator + how results are measured/calculated. | 59.0 |
| **IndicatorAssignment** | Assignment of an indicator to measure an outcome/activity. | 59.0 |
| **IndicatorPerformancePeriod** | A time period + frequency for calculating indicator results (baseline). | 59.0 |
| **IndicatorResult** | Result of an indicator assignment for a period. | 59.0 |
| **PartyIndicatorResult** | The party for which an indicator result is calculated. | 62.0 |
| **Outcome** | Expected change in participants driven by org activity. | 59.0 |
| **OutcomeActivity** | Junction — Outcome ↔ related activity object. | 59.0 |

## Device Sync / Mobile (offline)

| Object | Purpose | Since |
|---|---|---|
| **DeviceSyncSummary** | Summary of synchronized data from a mobile device. | 65.0 |
| **DeviceSyncTransaction** | A set of related data items to sync from a device. | 65.0 |
| **DeviceSyncTransactionRecord** | A single data item to sync from a device. | 65.0 |
| **DeviceSyncTransactionLog** | Log of synchronized data from a device. | 65.0 |
| **LifeScienceMobileApp** | Info about a mobile device associated with a user. | 65.0 |
| **LifeSciMobileMetadataRecord** | Metadata created for the mobile application. | 65.0 |

## Video Calls (remote engagement)

| Object | Purpose | Since |
|---|---|---|
| **VideoCall** | A video call (meeting ID, duration, participants, recordings, vendor attrs) (LSC-extended). | 65.0 |
| **VideoCallParticipant** | A participant of a video call (provider- or Salesforce-sourced). | 65.0 |
| **VideoCallRecording** | A recording from a video call (video/voice/transcript). | 65.0 |
| **VideoCallPtcpRequest** | Remote signature request for video-call participants. | 65.0 |
| **VideoCallPtcpSession** | Participant remote-session info (duration, device, OS, browser). | 65.0 |

## Data Change Requests / Data Governance

| Object | Purpose | Since |
|---|---|---|
| **LifeSciDataChangeDef** | The object a data-change request is configured for. | 65.0 |
| **LifeSciDataChangeRequest** | Data-change requests for all objects. | 65.0 |
| **LifeSciDataChgDefMngFld** | Fields a data-change request is configured for. | 65.0 |
| **LifeSciDataChgDefRecType** | Data validation for the object by record type. | |
| **LifeSciDataChgPersonaDef** | Data-update config for the object by persona. | |

## Workflow / Stage Management & Work Procedures

| Object | Purpose | Since |
|---|---|---|
| **LifeSciStageObject** | An object associated with a workflow. | 65.0 |
| **LifeSciStageValue** | An individual step within a workflow. | 65.0 |
| **LifeSciStagePath** | Steps in a workflow and the path from one step to the next. | 65.0 |
| **LifeSciStageAction** | Config of an action performed as part of a workflow. | 65.0 |
| **LifeSciStageOperation** | Criteria for permissions/available actions at a workflow step. | 65.0 |
| **LifeSciStageOperationAction** | Junction — stage operation ↔ stage action. | 65.0 |
| **LifeSciStageOperationCondn** | Logical expression for applying a workflow operation. | 65.0 |
| **LifeScienceCustomScript** | Custom script for a stage object's validation logic. | 65.0 |
| **LifeScienceTriggerHandler** | Trigger handlers to run for each LSC object. | 65.0 |
| **WorkProcedure** | A procedure/process that's part of a program. | |
| **WorkProcedureStep** | A work type that's part of a work procedure. | |
| **WorkTypeExtension** | Additional info about a work type. | |
| **WorkTypeStep** | Each step within a work type. | |
| **WorkTypeStepLdTimeOvride** | Lead-time override for a procedure/type/step at a service territory. | 59.0 |
| **WorkTypeSvcTerrSchdPrio** | Priority of service-territory + work-type + procedure for slot fetching. | 59.0 |
| **ServiceAppointmentGroup** | A group of related service appointments. | 56.0 |

## Metadata / Configuration Framework

| Object | Purpose | Since |
|---|---|---|
| **LifeSciMetadataCategory** | Category that LSC configuration records are organized into. | 65.0 |
| **LifeSciMetadataRecord** | A configuration record for LSC (child of category). | 65.0 |
| **LifeSciMetadataAssignment** | Assignments for a config record (child of record). | 65.0 |
| **LifeSciMetadataFieldValue** | A field value for a config record (child of record). | 65.0 |
| **BatchJob** | An instance of a running/run batch job. | 65.0 |
| **BatchJobPart** | One part of a batch job. | 65.0 |

## Documents (Intake)

| Object | Purpose | Since |
|---|---|---|
| **ReceivedDocument** | A request for a document operation (rotate/split/text extraction). | 50.0 |
| **ReceivedDocumentType** | Junction — Received Document ↔ Document Type. | 58.0 |

---

## Beyond the object list

The dev guide's data-model section has adjacent references not enumerated here —
fetch on demand when a story needs them:

- **Associated Objects** — objects associated with LSC standard objects, with their standard fields:
  [Associated Objects](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_sforce_api_associated_objects_list.htm)
- **Fields on Standard Objects** — LSC fields *added* to core Salesforce objects (Account, Contact, etc.), available only when LSC is enabled:
  [Fields on Standard Objects](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/life_sciences_sforce_api_fields.htm)
- **StandardValueSet Names & Standard Picklist Fields**, **Platform Events**, **Tooling API Objects**, **Metadata Types** — see the
  [Data Models overview](https://developer.salesforce.com/docs/atlas.en-us.life_sciences_dev_guide.meta/life_sciences_dev_guide/lsc_data_models_overview.htm).

**Field verification is mandatory:** the dev guide does not list every field per
object. Before you name a field in a story, run a `describe` in an LSC-enabled
org, inspect the WSDL, or use a schema viewer (SKILL RULE 3). In this PNM
workspace, mark any unverifiable object/field as *proposed*.

---

## Provenance

| Item | Value |
|---|---|
| Source | Life Sciences Cloud Developer Guide → *Life Sciences Cloud Standard Objects* |
| Release | Summer '26 |
| API version | 67.0 (labelled "Latest" at capture) |
| Captured | 2026-07-30 |
| Object count | ~350 standard objects |
| Caveat | Field lists are not in the guide — verify via `describe`/WSDL/schema viewer. |
