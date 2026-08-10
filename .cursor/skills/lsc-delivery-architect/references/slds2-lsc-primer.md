# SLDS 2 + Cosmos Primer for LSC Prototypes

> **Purpose.** This is the LSC Delivery Architect's **curated Salesforce Lightning
> Design System (SLDS) 2 + Cosmos theme** primer for grounded HTML prototypes
> (§6.7). Every clickable prototype the skill produces MUST be styled with the
> hooks, utilities, and blueprint recipes in this file — not with generic web
> CSS, not with SLDS 1, and not with hand-invented class names.
>
> **Distilled from** the Salesforce Experience UX plugin
> [`design-quality-experiences/applying-slds`](https://git.soma.salesforce.com/codeai/awesome-context/tree/main/plugins/design-quality-experiences)
> (source: `github.com/salesforce-ux-emu/design-intelligence/packages/skills/applying-slds`).
> Only the hooks, utilities, and blueprints an LSC prototype actually uses.
> Provenance and update policy at the bottom of this file.
>
> **Scope.** Everything you need to hand-author a Salesforce-looking HTML file
> for a PO walkthrough. Deliberately *not* covered: LWC mechanics (`@wire`,
> `@api`, lifecycle); production accessibility gates (we ship a lightweight
> a11y checklist here, not full WCAG conformance); the SLDS linter (we do not
> vendor the Node linter — see §*Verification (score-only)*).
>
> **What this primer does not replace.** If the full
> `design-quality-experiences` plugin is ever installed in the workspace, we
> can swap up to it for verified compliance scoring. Until then, this primer
> is the source of truth.

---

## 1. How to open an LSC prototype

Every prototype file starts with **the Cosmos CSS variable block**, then real
SLDS 2 markup. No CDN, no external stylesheet — self-contained.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title><Capability> — LSC Prototype (Salesforce Life Sciences Cloud)</title>
<style>
  /* ---------- SLDS 2 + Cosmos: essential styling hooks (light-mode defaults) ---------- */
  :root {
    /* Colour — surface (85%) */
    --slds-g-color-surface-1: #ffffff;
    --slds-g-color-surface-2: #f3f3f3;
    --slds-g-color-surface-3: #e5e5e5;
    --slds-g-color-surface-container-1: #ffffff;
    --slds-g-color-surface-container-2: #f3f3f3;
    --slds-g-color-on-surface-1: #747474;   /* low emphasis */
    --slds-g-color-on-surface-2: #181818;   /* body text */
    --slds-g-color-on-surface-3: #080707;   /* headings */

    /* Colour — accent (5%) */
    --slds-g-color-accent-1: #0176d3;       /* Salesforce blue */
    --slds-g-color-accent-2: #014486;
    --slds-g-color-accent-container-1: #0176d3;
    --slds-g-color-on-accent-1: #ffffff;
    --slds-g-color-on-accent-2: #f3f3f3;

    /* Colour — feedback */
    --slds-g-color-success-1: #2e844a;
    --slds-g-color-on-success-1: #ffffff;
    --slds-g-color-warning-1: #fe9339;
    --slds-g-color-on-warning-1: #080707;
    --slds-g-color-error-1: #ba0517;
    --slds-g-color-on-error-1: #ffffff;

    /* Colour — border */
    --slds-g-color-border-1: #c9c9c9;
    --slds-g-color-border-2: #aeaeae;

    /* Spacing (4-point grid) */
    --slds-g-spacing-1: 0.25rem;   /* 4  */
    --slds-g-spacing-2: 0.5rem;    /* 8  */
    --slds-g-spacing-3: 0.75rem;   /* 12 */
    --slds-g-spacing-4: 1rem;      /* 16 */
    --slds-g-spacing-5: 1.5rem;    /* 24 */
    --slds-g-spacing-6: 2rem;      /* 32 */
    --slds-g-spacing-8: 3rem;      /* 48 */
    --slds-g-spacing-12: 5rem;     /* 80 */

    /* Typography */
    --slds-g-font-family-base: "Salesforce Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --slds-g-font-size-base: 0.8125rem;   /* 13px */
    --slds-g-font-scale-neg-1: 0.75rem;   /* 12px */
    --slds-g-font-scale-1: 0.875rem;      /* 14px */
    --slds-g-font-scale-2: 1rem;          /* 16px */
    --slds-g-font-scale-3: 1.125rem;      /* 18px */
    --slds-g-font-scale-4: 1.25rem;       /* 20px */
    --slds-g-font-scale-6: 1.75rem;       /* 28px */
    --slds-g-font-scale-8: 2.5rem;        /* 40px */
    --slds-g-font-weight-4: 400;
    --slds-g-font-weight-5: 500;
    --slds-g-font-weight-7: 700;

    /* Radius */
    --slds-g-radius-border-1: 0.125rem;
    --slds-g-radius-border-2: 0.25rem;
    --slds-g-radius-border-3: 0.5rem;
    --slds-g-radius-border-circle: 50%;

    /* Shadow */
    --slds-g-shadow-1: 0 2px 4px rgba(0, 0, 0, 0.08);
    --slds-g-shadow-2: 0 2px 8px rgba(0, 0, 0, 0.16);
    --slds-g-shadow-inset-1: inset 0 0 0 1px var(--slds-g-color-border-1);

    /* Duration */
    --slds-g-duration-1: 150ms;
    --slds-g-duration-2: 250ms;
  }

  /* Baseline document */
  html, body { margin: 0; padding: 0; }
  body {
    font-family: var(--slds-g-font-family-base);
    font-size: var(--slds-g-font-size-base);
    color: var(--slds-g-color-on-surface-2, #181818);
    background: var(--slds-g-color-surface-2, #f3f3f3);
    line-height: 1.4;
  }

  /* Ship the SLDS utility helpers this primer relies on inline (§4) */
  /* See §4 of the primer for the full list; keep only the classes you use */
</style>
</head>
<body>
  <!-- LSC prototype content — real SLDS 2 markup goes here -->
</body>
</html>
```

**Why inline the tokens?** Product owners open the file locally, email it,
zip it, or drop it into Confluence. A CDN link that requires internal auth or
network access would break the emailable single-file contract from §6.7.

---

## 2. The colour rules (85 · 5 · 10)

| % | Role | Hook family | Where in LSC |
|---|------|-------------|--------------|
| **85 %** | Surface, background, container | `--slds-g-color-surface-*` / `--slds-g-color-surface-container-*` | Page background, cards, modals, related lists |
| **5 %** | Accent, primary CTA, selected state | `--slds-g-color-accent-*` / `--slds-g-color-accent-container-*` | "Save", "New Visit", "Log Inquiry", selected tab |
| **10 %** | Expressive · data viz · brand | palette hooks (not covered here) | Sample-inventory bar chart, KAM plan score gauge |

### Pair surface with on-surface

Every surface needs a legible text colour paired with it:

| Surface | On-surface pair | Example |
|---------|-----------------|---------|
| `surface-1` | `on-surface-2` | Card body text on white |
| `surface-2` | `on-surface-2` | Page background text |
| `accent-1`  | `on-accent-1`  | Text on the "Save" button |
| `success-1` | `on-success-1` | Text on a green confirmation banner |
| `error-1`   | `on-error-1`   | Text on a red error banner |

### Numbered variants — pick emphasis, not shade

Every `--slds-g-color-*` hook ends in a number. Higher = more emphasis, **not**
darker. There is no unnumbered base form.

| Variant | Emphasis | Use |
|---------|----------|-----|
| `-1` | Low | Captions, placeholder text, secondary metadata |
| `-2` | Medium | Body text, labels, standard content |
| `-3` | High | Page titles, headings, primary emphasis |

---

## 3. Spacing (4-point grid)

Use the **utility classes** in markup wherever possible (§4). Fall back to the
hooks when you need custom CSS.

| Hook | Value | Pixels | Use |
|------|-------|--------|-----|
| `--slds-g-spacing-1` | 0.25rem | 4  | Tight inline spacing between an icon and its label |
| `--slds-g-spacing-2` | 0.5rem  | 8  | Gap between related items in a list |
| `--slds-g-spacing-3` | 0.75rem | 12 | Compact card padding |
| `--slds-g-spacing-4` | 1rem    | 16 | **Standard** — default padding, default margin |
| `--slds-g-spacing-5` | 1.5rem  | 24 | Section spacing |
| `--slds-g-spacing-6` | 2rem    | 32 | Between sections on a page |
| `--slds-g-spacing-8` | 3rem    | 48 | Large separations (e.g. above the page footer) |
| `--slds-g-spacing-12` | 5rem   | 80 | Page-level spacing (rare in LSC prototypes) |

---

## 4. Utility classes worth inlining

Ship **only these ~25 helper rules** in the prototype's `<style>` block —
enough for 95 % of LSC screens without pulling the full 1,147-class SLDS
utility bundle.

```css
/* Grid */
.slds-grid              { display: flex; flex-wrap: nowrap; }
.slds-wrap              { flex-wrap: wrap; }
.slds-grid_vertical     { display: flex; flex-direction: column; }
.slds-gutters > .slds-col { padding-left: var(--slds-g-spacing-3); padding-right: var(--slds-g-spacing-3); }
.slds-col               { flex: 1 1 auto; min-width: 0; }
.slds-grid_align-center { justify-content: center; }
.slds-grid_align-end    { justify-content: flex-end; }
.slds-grid_vertical-align-center { align-items: center; }

/* Fractional sizing (add the ones you use) */
.slds-size_1-of-1  { width: 100%; }
.slds-size_1-of-2  { width: 50%; }
.slds-size_1-of-3  { width: 33.333%; }
.slds-size_2-of-3  { width: 66.666%; }
.slds-size_1-of-4  { width: 25%; }
.slds-size_3-of-4  { width: 75%; }

/* Margin (add the ones you use) */
.slds-m-around_x-small  { margin: var(--slds-g-spacing-2); }
.slds-m-around_small    { margin: var(--slds-g-spacing-3); }
.slds-m-around_medium   { margin: var(--slds-g-spacing-4); }
.slds-m-bottom_x-small  { margin-bottom: var(--slds-g-spacing-2); }
.slds-m-bottom_small    { margin-bottom: var(--slds-g-spacing-3); }
.slds-m-bottom_medium   { margin-bottom: var(--slds-g-spacing-4); }
.slds-m-bottom_large    { margin-bottom: var(--slds-g-spacing-5); }
.slds-m-top_medium      { margin-top: var(--slds-g-spacing-4); }
.slds-m-right_x-small   { margin-right: var(--slds-g-spacing-2); }
.slds-m-right_small     { margin-right: var(--slds-g-spacing-3); }
.slds-m-left_small      { margin-left: var(--slds-g-spacing-3); }

/* Padding (add the ones you use) */
.slds-p-around_x-small  { padding: var(--slds-g-spacing-2); }
.slds-p-around_small    { padding: var(--slds-g-spacing-3); }
.slds-p-around_medium   { padding: var(--slds-g-spacing-4); }
.slds-p-around_large    { padding: var(--slds-g-spacing-5); }
.slds-p-vertical_small  { padding-top: var(--slds-g-spacing-3); padding-bottom: var(--slds-g-spacing-3); }
.slds-p-horizontal_medium { padding-left: var(--slds-g-spacing-4); padding-right: var(--slds-g-spacing-4); }

/* Typography */
.slds-text-heading_small  { font-size: var(--slds-g-font-scale-2); font-weight: var(--slds-g-font-weight-5); color: var(--slds-g-color-on-surface-3); }
.slds-text-heading_medium { font-size: var(--slds-g-font-scale-4); font-weight: var(--slds-g-font-weight-5); color: var(--slds-g-color-on-surface-3); }
.slds-text-heading_large  { font-size: var(--slds-g-font-scale-6); font-weight: var(--slds-g-font-weight-5); color: var(--slds-g-color-on-surface-3); }
.slds-text-body_regular   { font-size: var(--slds-g-font-scale-1); color: var(--slds-g-color-on-surface-2); }
.slds-text-body_small     { font-size: var(--slds-g-font-scale-neg-1); color: var(--slds-g-color-on-surface-1); }
.slds-text-title          { font-size: var(--slds-g-font-scale-neg-1); text-transform: uppercase; letter-spacing: 0.04em; color: var(--slds-g-color-on-surface-1); font-weight: var(--slds-g-font-weight-7); }
.slds-text-color_weak     { color: var(--slds-g-color-on-surface-1); }

/* Visibility */
.slds-hide                { display: none !important; }
.slds-show                { display: block !important; }
.slds-assistive-text      { position: absolute !important; margin: -1px !important; border: 0 !important; padding: 0 !important; width: 1px !important; height: 1px !important; overflow: hidden !important; clip: rect(0 0 0 0) !important; }

/* Truncation */
.slds-truncate            { max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
```

**Rule of thumb:** copy only the rules you actually use into a given prototype
so the file stays small (< 100 KB). The reference above is the master list.

---

## 5. Blueprint recipes an LSC prototype needs

Twelve blueprints cover 95 % of LSC screens. Every recipe below is the real
SLDS 2 markup — copy-paste, adjust the content, keep the class names.

### 5.1 Page header (record page top)

```html
<header class="slds-page-header">
  <div class="slds-page-header__row">
    <div class="slds-page-header__col-title">
      <div class="slds-grid">
        <div class="slds-icon-container slds-icon-container_circle slds-p-around_x-small"
             style="background: var(--slds-g-color-accent-container-1);">
          <span class="slds-assistive-text">Visit</span>
          <!-- 24×24 SVG icon — see §6 -->
          <svg width="24" height="24" fill="var(--slds-g-color-on-accent-1)" aria-hidden="true">
            <use href="#icon-visit"></use>
          </svg>
        </div>
        <div class="slds-m-left_small">
          <p class="slds-text-title">Visit</p>
          <h1 class="slds-text-heading_medium slds-truncate" title="Dr. Reddy — 15 Aug 2026">
            Dr. Reddy — 15 Aug 2026
          </h1>
        </div>
      </div>
    </div>
    <div class="slds-page-header__col-actions">
      <div class="slds-grid slds-grid_align-end">
        <button class="slds-button slds-button_neutral slds-m-right_x-small">Edit</button>
        <button class="slds-button slds-button_brand">Save</button>
      </div>
    </div>
  </div>
</header>
```

Add `.slds-page-header`, `.slds-page-header__row`, `.slds-page-header__col-title`,
`.slds-page-header__col-actions`, `.slds-icon-container`, `.slds-button`,
`.slds-button_neutral`, `.slds-button_brand` to your inline style block (see §7
for the CSS).

### 5.2 Path (record process stages)

```html
<div class="slds-path">
  <ul class="slds-path__nav">
    <li class="slds-path__item slds-is-complete">
      <a class="slds-path__link"><span class="slds-path__title">Planned</span></a>
    </li>
    <li class="slds-path__item slds-is-current slds-is-active">
      <a class="slds-path__link"><span class="slds-path__title">In progress</span></a>
    </li>
    <li class="slds-path__item slds-is-incomplete">
      <a class="slds-path__link"><span class="slds-path__title">Completed</span></a>
    </li>
    <li class="slds-path__item slds-is-incomplete">
      <a class="slds-path__link"><span class="slds-path__title">Approved</span></a>
    </li>
  </ul>
</div>
```

### 5.3 Tabs (record page content sections)

```html
<div class="slds-tabs_default">
  <ul class="slds-tabs_default__nav" role="tablist">
    <li class="slds-tabs_default__item slds-is-active" role="presentation">
      <a class="slds-tabs_default__link" role="tab" tabindex="0" aria-selected="true">Details</a>
    </li>
    <li class="slds-tabs_default__item" role="presentation">
      <a class="slds-tabs_default__link" role="tab" tabindex="-1" aria-selected="false">Samples</a>
    </li>
    <li class="slds-tabs_default__item" role="presentation">
      <a class="slds-tabs_default__link" role="tab" tabindex="-1" aria-selected="false">Expenses</a>
    </li>
  </ul>
  <div class="slds-tabs_default__content slds-show" role="tabpanel">
    <!-- Active tab content -->
  </div>
</div>
```

### 5.4 Card

```html
<article class="slds-card">
  <div class="slds-card__header slds-grid">
    <header class="slds-media slds-media_center slds-has-flexi-truncate">
      <div class="slds-media__body">
        <h2 class="slds-card__header-title slds-text-heading_small">HCP context</h2>
      </div>
    </header>
    <div class="slds-no-flex">
      <button class="slds-button slds-button_neutral">View profile</button>
    </div>
  </div>
  <div class="slds-card__body slds-card__body_inner">
    <!-- card content -->
  </div>
  <footer class="slds-card__footer">
    <a>View all</a>
  </footer>
</article>
```

### 5.5 Form (label + input)

```html
<div class="slds-form-element">
  <label class="slds-form-element__label" for="visit-notes">Visit notes</label>
  <div class="slds-form-element__control">
    <textarea id="visit-notes" class="slds-textarea" rows="4"
              placeholder="Discussed dosing schedule and side-effect profile"></textarea>
  </div>
</div>

<div class="slds-form-element slds-m-top_medium">
  <label class="slds-form-element__label" for="hcp">Attendee (HCP)</label>
  <div class="slds-form-element__control">
    <div class="slds-combobox_container">
      <input id="hcp" class="slds-input" type="text" value="Dr. Anita Reddy" />
    </div>
  </div>
</div>
```

### 5.6 Data table

```html
<table class="slds-table slds-table_bordered slds-table_cell-buffer">
  <thead>
    <tr class="slds-line-height_reset">
      <th scope="col"><div class="slds-truncate" title="Product">Product</div></th>
      <th scope="col"><div class="slds-truncate" title="Lot">Lot</div></th>
      <th scope="col"><div class="slds-truncate" title="Quantity">Quantity</div></th>
      <th scope="col"><div class="slds-truncate" title="Expires">Expires</div></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row"><div class="slds-truncate" title="Cardizex 10 mg">Cardizex 10 mg</div></th>
      <td><div class="slds-truncate">L-2026-088</div></td>
      <td><div class="slds-truncate">4 units</div></td>
      <td><div class="slds-truncate">28 Feb 2027</div></td>
    </tr>
  </tbody>
</table>
```

### 5.7 Buttons

```html
<!-- Primary action -->
<button class="slds-button slds-button_brand">Log inquiry</button>

<!-- Secondary action -->
<button class="slds-button slds-button_neutral">Cancel</button>

<!-- Destructive action -->
<button class="slds-button slds-button_destructive">Delete visit</button>

<!-- Icon button (compact action) -->
<button class="slds-button slds-button_icon slds-button_icon-border-filled" title="Edit">
  <svg width="14" height="14" aria-hidden="true"><use href="#icon-edit"></use></svg>
  <span class="slds-assistive-text">Edit</span>
</button>
```

### 5.8 Modal

```html
<section role="dialog" aria-modal="true" class="slds-modal slds-fade-in-open">
  <div class="slds-modal__container">
    <header class="slds-modal__header">
      <h2 class="slds-modal__title slds-text-heading_medium">Sample drop — HCP e-signature</h2>
    </header>
    <div class="slds-modal__content slds-p-around_medium">
      <!-- content -->
    </div>
    <footer class="slds-modal__footer">
      <button class="slds-button slds-button_neutral">Cancel</button>
      <button class="slds-button slds-button_brand">Capture signature</button>
    </footer>
  </div>
</section>
<div class="slds-backdrop slds-backdrop_open"></div>
```

### 5.9 Alert / scoped notification

```html
<div class="slds-notify slds-notify_alert slds-theme_success" role="alert">
  <span class="slds-assistive-text">Success</span>
  <h2>Visit saved. Sample transaction recorded (Lot L-2026-088, 4 units).</h2>
</div>

<div class="slds-notify slds-notify_alert slds-theme_error" role="alert">
  <span class="slds-assistive-text">Error</span>
  <h2>Sample drop blocked — HCP licence is not valid in this state.</h2>
</div>
```

### 5.10 Related list

```html
<div class="slds-card">
  <header class="slds-card__header slds-grid">
    <h2 class="slds-text-heading_small">Sample transactions (3)</h2>
    <div class="slds-no-flex">
      <button class="slds-button slds-button_neutral">New</button>
    </div>
  </header>
  <div class="slds-card__body">
    <!-- Use the data table recipe from §5.6 -->
  </div>
</div>
```

### 5.11 Empty state

```html
<div class="slds-illustration slds-illustration_small slds-p-around_large slds-text-align_center">
  <h3 class="slds-text-heading_small">No sample transactions yet</h3>
  <p class="slds-text-body_regular slds-m-top_x-small">
    Sample drops recorded during this visit will appear here.
  </p>
  <button class="slds-button slds-button_brand slds-m-top_medium">Add sample drop</button>
</div>
```

### 5.12 Global action bar (top of app)

```html
<header class="slds-global-header slds-grid slds-grid_align-spread slds-p-around_x-small"
        style="background: var(--slds-g-color-on-surface-3); color: var(--slds-g-color-on-accent-1);">
  <div class="slds-global-header__logo slds-text-title">Life Sciences Cloud</div>
  <div class="slds-grid slds-grid_align-end">
    <span class="slds-m-right_small">Field Sales Rep · Anita Menon</span>
    <button class="slds-button slds-button_icon"
            style="color: var(--slds-g-color-on-accent-1);">
      <svg width="16" height="16" aria-hidden="true"><use href="#icon-user"></use></svg>
    </button>
  </div>
</header>
```

---

## 6. Icon vocabulary for LSC

Salesforce ships 1,732 SVG icons across five categories (`action`, `custom`,
`doctype`, `standard`, `utility`). LSC prototypes need ~50. Use inline SVG
with a `<symbol>`-based sprite so the file stays self-contained.

### Icon set to ship inline

Give each LSC prototype this small sprite block near the top of `<body>`:

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <!-- LSC standard-icon glyph placeholders — use real SLDS SVG paths in production -->
  <symbol id="icon-visit"     viewBox="0 0 24 24"><path d="M3 5h18v14H3z M7 9h10 M7 13h10 M7 17h6" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-sample"    viewBox="0 0 24 24"><path d="M9 3h6v6l4 12H5l4-12z" fill="currentColor"/></symbol>
  <symbol id="icon-account"   viewBox="0 0 24 24"><circle cx="12" cy="9" r="4" fill="currentColor"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7" fill="currentColor"/></symbol>
  <symbol id="icon-product"   viewBox="0 0 24 24"><path d="M4 8l8-5 8 5v9l-8 5-8-5z" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-event"     viewBox="0 0 24 24"><path d="M5 4h14v16H5z M5 8h14 M8 2v4 M16 2v4" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-inquiry"   viewBox="0 0 24 24"><path d="M4 4h16v12H8l-4 4z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="1" fill="currentColor"/></symbol>
  <symbol id="icon-hcp"       viewBox="0 0 24 24"><path d="M12 2l3 6h6l-5 4 2 8-6-4-6 4 2-8-5-4h6z" fill="currentColor"/></symbol>
  <symbol id="icon-payer"     viewBox="0 0 24 24"><path d="M4 6h16v12H4z M4 10h16 M8 14h4" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-alert"     viewBox="0 0 24 24"><path d="M12 3l10 18H2z M12 10v5 M12 17h.01" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-user"      viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="currentColor"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6" fill="currentColor"/></symbol>
  <symbol id="icon-edit"      viewBox="0 0 14 14"><path d="M2 12l1-3 6-6 3 3-6 6z" fill="currentColor"/></symbol>
</svg>
```

> **Fidelity note.** In a production build you would substitute the real
> Salesforce SVG paths from `@salesforce-ux/design-system-2/assets/icons/`.
> For PO prototypes the simplified glyphs above are acceptable and keep the
> file portable. Document this in the prototype's build-tech banner.

### LSC noun → icon map

| LSC noun | Icon id | Category |
|----------|---------|----------|
| Visit / Call | `#icon-visit` | standard:visit |
| Sample / drug sample | `#icon-sample` | standard:sample_management |
| Account · HCP · HCO | `#icon-account` / `#icon-hcp` | standard:account · standard:hcp |
| Product / drug | `#icon-product` | standard:product |
| Event / Managed Event | `#icon-event` | standard:event |
| Medical Inquiry | `#icon-inquiry` | standard:case |
| KOL / DOL | `#icon-hcp` | standard:individual |
| Payer / Plan / Formulary | `#icon-payer` | standard:orders |
| Alert · Adverse Event · Compliance | `#icon-alert` | utility:warning |
| Person / running user | `#icon-user` | utility:user |
| Edit / Save inline | `#icon-edit` | utility:edit |

---

## 7. Component styles to ship inline

Add these to the prototype's `<style>` block. These are the SLDS 2 shapes for
the blueprints in §5 — no LWC dependency.

```css
/* Buttons */
.slds-button {
  display: inline-flex; align-items: center; justify-content: center;
  border: 1px solid transparent; border-radius: var(--slds-g-radius-border-2);
  padding: 0 var(--slds-g-spacing-3); height: 2rem;
  font-family: inherit; font-size: var(--slds-g-font-scale-1); font-weight: var(--slds-g-font-weight-5);
  cursor: pointer; transition: background var(--slds-g-duration-1);
}
.slds-button_brand       { background: var(--slds-g-color-accent-1); color: var(--slds-g-color-on-accent-1); }
.slds-button_brand:hover { background: var(--slds-g-color-accent-2); }
.slds-button_neutral     { background: var(--slds-g-color-surface-1); color: var(--slds-g-color-accent-1);
                           border-color: var(--slds-g-color-border-2); }
.slds-button_destructive { background: var(--slds-g-color-error-1); color: var(--slds-g-color-on-error-1); }
.slds-button_icon        { height: 2rem; width: 2rem; padding: 0; }
.slds-button_icon-border-filled { background: var(--slds-g-color-surface-1); border-color: var(--slds-g-color-border-2); }

/* Card */
.slds-card { background: var(--slds-g-color-surface-container-1); border: 1px solid var(--slds-g-color-border-1);
             border-radius: var(--slds-g-radius-border-2); box-shadow: var(--slds-g-shadow-1); }
.slds-card__header { padding: var(--slds-g-spacing-4); align-items: center; }
.slds-card__body   { padding: 0 var(--slds-g-spacing-4) var(--slds-g-spacing-4); }
.slds-card__body_inner { padding: var(--slds-g-spacing-4); }
.slds-card__header-title { font-weight: var(--slds-g-font-weight-5); }
.slds-card__footer { padding: var(--slds-g-spacing-3) var(--slds-g-spacing-4);
                     border-top: 1px solid var(--slds-g-color-border-1); text-align: center; }

/* Page header */
.slds-page-header { background: var(--slds-g-color-surface-1); padding: var(--slds-g-spacing-4);
                    border-bottom: 1px solid var(--slds-g-color-border-1); }
.slds-page-header__row { display: flex; align-items: center; justify-content: space-between; gap: var(--slds-g-spacing-4); }
.slds-page-header__col-title { min-width: 0; flex: 1 1 auto; }
.slds-page-header__col-actions { flex: 0 0 auto; }
.slds-icon-container_circle { border-radius: var(--slds-g-radius-border-circle); display: inline-flex; }

/* Tabs */
.slds-tabs_default__nav { display: flex; border-bottom: 1px solid var(--slds-g-color-border-1); list-style: none; margin: 0; padding: 0; }
.slds-tabs_default__item { margin-right: var(--slds-g-spacing-4); }
.slds-tabs_default__link { display: block; padding: var(--slds-g-spacing-3) 0; color: var(--slds-g-color-on-surface-1);
                           border-bottom: 2px solid transparent; text-decoration: none; cursor: pointer; }
.slds-tabs_default__item.slds-is-active .slds-tabs_default__link {
  color: var(--slds-g-color-accent-1); border-bottom-color: var(--slds-g-color-accent-1); font-weight: var(--slds-g-font-weight-5);
}
.slds-tabs_default__content { padding: var(--slds-g-spacing-4) 0; }

/* Path */
.slds-path { background: var(--slds-g-color-surface-1); border: 1px solid var(--slds-g-color-border-1);
             border-radius: var(--slds-g-radius-border-2); padding: var(--slds-g-spacing-3); }
.slds-path__nav { display: flex; list-style: none; margin: 0; padding: 0; gap: var(--slds-g-spacing-1); }
.slds-path__item { flex: 1 1 0; }
.slds-path__link { display: block; padding: var(--slds-g-spacing-2) var(--slds-g-spacing-3);
                   background: var(--slds-g-color-surface-2); border-radius: var(--slds-g-radius-border-1);
                   text-decoration: none; color: var(--slds-g-color-on-surface-2); text-align: center;
                   font-size: var(--slds-g-font-scale-neg-1); }
.slds-path__item.slds-is-complete .slds-path__link { background: var(--slds-g-color-success-1); color: var(--slds-g-color-on-success-1); }
.slds-path__item.slds-is-current  .slds-path__link { background: var(--slds-g-color-accent-1);  color: var(--slds-g-color-on-accent-1); font-weight: var(--slds-g-font-weight-5); }

/* Table */
.slds-table { width: 100%; border-collapse: collapse; background: var(--slds-g-color-surface-1); font-size: var(--slds-g-font-scale-1); }
.slds-table th, .slds-table td { text-align: left; padding: var(--slds-g-spacing-3); }
.slds-table thead th { background: var(--slds-g-color-surface-2); color: var(--slds-g-color-on-surface-1);
                       font-weight: var(--slds-g-font-weight-7); text-transform: uppercase; letter-spacing: 0.04em;
                       font-size: var(--slds-g-font-scale-neg-1); border-bottom: 1px solid var(--slds-g-color-border-1); }
.slds-table_bordered td, .slds-table_bordered th { border-bottom: 1px solid var(--slds-g-color-border-1); }

/* Form */
.slds-form-element__label { display: block; font-size: var(--slds-g-font-scale-neg-1);
                            font-weight: var(--slds-g-font-weight-5); color: var(--slds-g-color-on-surface-1);
                            margin-bottom: var(--slds-g-spacing-1); }
.slds-input, .slds-textarea, .slds-combobox_container input {
  width: 100%; padding: var(--slds-g-spacing-2) var(--slds-g-spacing-3);
  font-family: inherit; font-size: var(--slds-g-font-scale-1); color: var(--slds-g-color-on-surface-2);
  background: var(--slds-g-color-surface-1);
  border: 1px solid var(--slds-g-color-border-2); border-radius: var(--slds-g-radius-border-2);
}
.slds-input:focus, .slds-textarea:focus { outline: none; border-color: var(--slds-g-color-accent-1);
                                          box-shadow: 0 0 0 3px rgba(1, 118, 211, 0.20); }

/* Modal */
.slds-modal { position: fixed; inset: 4rem 0 0 0; z-index: 9002; display: flex; justify-content: center; }
.slds-modal__container { background: var(--slds-g-color-surface-1); border-radius: var(--slds-g-radius-border-3);
                         box-shadow: var(--slds-g-shadow-2); width: min(720px, calc(100vw - 4rem)); max-height: calc(100vh - 8rem);
                         display: flex; flex-direction: column; overflow: hidden; }
.slds-modal__header  { padding: var(--slds-g-spacing-4); border-bottom: 1px solid var(--slds-g-color-border-1); }
.slds-modal__content { padding: var(--slds-g-spacing-4); overflow: auto; }
.slds-modal__footer  { padding: var(--slds-g-spacing-4); border-top: 1px solid var(--slds-g-color-border-1);
                       display: flex; justify-content: flex-end; gap: var(--slds-g-spacing-2); }
.slds-backdrop { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); z-index: 9001; }

/* Alerts (scoped notifications) */
.slds-notify_alert { padding: var(--slds-g-spacing-3) var(--slds-g-spacing-4);
                     border-radius: var(--slds-g-radius-border-2); font-size: var(--slds-g-font-scale-1); }
.slds-theme_success { background: var(--slds-g-color-success-1); color: var(--slds-g-color-on-success-1); }
.slds-theme_error   { background: var(--slds-g-color-error-1);   color: var(--slds-g-color-on-error-1); }
.slds-theme_warning { background: var(--slds-g-color-warning-1); color: var(--slds-g-color-on-warning-1); }
```

---

## 8. LSC build-technology overlay — the badging layer

**This is what makes an LSC prototype different from a stock SLDS 2 mockup.**
Every interactive element must carry a small badge naming the Salesforce
component that will implement it, per §6.7 hard-blocker #2.

### Ship this on top of the SLDS 2 markup

```css
/* Build-tech badges (LSC-specific overlay) */
.lsc-badge {
  display: inline-flex; align-items: center;
  font-size: 10px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase;
  padding: 2px 6px; margin-left: var(--slds-g-spacing-2);
  border-radius: var(--slds-g-radius-border-1); border: 1px solid var(--slds-g-color-border-1);
  color: var(--slds-g-color-on-surface-1); background: var(--slds-g-color-surface-2);
  vertical-align: middle;
}
.lsc-badge.ootb   { color: #2e844a; border-color: rgba(46,132,74,0.35);  background: rgba(46,132,74,0.10); }
.lsc-badge.config { color: #0176d3; border-color: rgba(1,118,211,0.35);  background: rgba(1,118,211,0.10); }
.lsc-badge.flow   { color: #7f5cff; border-color: rgba(127,92,255,0.35); background: rgba(127,92,255,0.10); }
.lsc-badge.lwc    { color: #b95500; border-color: rgba(185,85,0,0.35);   background: rgba(185,85,0,0.10); }
.lsc-badge.os     { color: #b8256b; border-color: rgba(184,37,107,0.35); background: rgba(184,37,107,0.10); }
.lsc-badge.apex   { color: #ba0517; border-color: rgba(186,5,23,0.35);   background: rgba(186,5,23,0.10); }
.lsc-badge.ext    { color: #514f4d; border-color: var(--slds-g-color-border-2); background: var(--slds-g-color-surface-3); }

/* Build-tech banner at the top of every LSC prototype */
.lsc-build-banner {
  background: var(--slds-g-color-accent-container-1); color: var(--slds-g-color-on-accent-1);
  padding: var(--slds-g-spacing-3) var(--slds-g-spacing-5);
  font-size: var(--slds-g-font-scale-1); line-height: 1.5;
}
.lsc-build-banner .lsc-build-title { font-weight: var(--slds-g-font-weight-7); letter-spacing: 0.02em; }
.lsc-build-banner .lsc-build-rejected { opacity: 0.85; }
```

### Badge naming vocabulary (LSC)

| Badge | Meaning | When to apply |
|-------|---------|---------------|
| `OOTB`   | Standard Salesforce out-of-the-box — no config change | Standard record page, standard related list, standard Path |
| `Config` | Declarative-only — Dynamic Actions, Field Sets, Page Layout, custom field | Custom action button added via Dynamic Actions; custom field on layout |
| `Flow`   | Screen Flow · Record-Triggered Flow · Subflow | Wizard screens, guided form, validation branching |
| `LWC`    | Lightning Web Component (custom code) | Signature pad, complex data-viz, offline component |
| `OS`     | OmniScript step | Branching guided intake (Medical Inquiry) |
| `Apex`   | Apex trigger, invocable, controller | Atomic multi-object writes, callouts |
| `Ext`    | External integration (MuleSoft · Concur · Data Cloud · e-signature vendor) | Concur expense sync, DAM content pull, Data Cloud feed |

### How to apply a badge

```html
<!-- On a button -->
<button class="slds-button slds-button_brand">
  Log inquiry
  <span class="lsc-badge os">OS</span>
</button>

<!-- On a heading -->
<h2 class="slds-text-heading_small">
  HCP context
  <span class="lsc-badge config">Config · FlexCard</span>
</h2>

<!-- On an entire section (top-right of a card) -->
<article class="slds-card" style="position: relative;">
  <span class="lsc-badge lwc" style="position: absolute; top: 8px; right: 8px;">LWC · signature pad</span>
  ...
</article>
```

**Rule:** **every interactive element** gets a badge. A single, top-of-page
"this whole thing is OOTB" is not enough — the PO's question is per-screen and
per-control.

### The build-tech banner

Every LSC prototype opens with this banner right below `<body>`, before any
SLDS chrome. It states the build-tech verdict from the story's
`Build Technology` header field:

```html
<div class="lsc-build-banner">
  <div class="lsc-build-title">Build technology · Mixed (OOTB + Dynamic Actions + Screen Flow + LWC signature pad + Apex)</div>
  <div class="lsc-build-rejected">Rejected: OmniScript — overkill for a single-screen action inside an existing record page.</div>
</div>
```

---

## 9. Worked LSC example — Sample Drop screen

A minimum-viable LSC prototype pattern combining a page header, path, tabs,
form, table, alert, and badges. Copy as the starting shell for any new
prototype.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>LSC Sample Drop — Field Sales Rep prototype</title>
<style>
  /* §1 root variables — pasted here in a real prototype */
  /* §4 utility classes — pasted here in a real prototype */
  /* §7 component styles — pasted here in a real prototype */
  /* §8 build-tech badges + banner — pasted here in a real prototype */
</style>
</head>
<body>
  <!-- Icon sprite (§6) -->
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"> ... </svg>

  <!-- Global header (§5.12) -->
  <header class="slds-global-header ...">Life Sciences Cloud</header>

  <!-- Build-tech banner (§8) -->
  <div class="lsc-build-banner">
    <div class="lsc-build-title">Build technology · Mixed — OOTB Visit record page + Dynamic Action + Screen Flow + LWC signature pad + Apex atomic write</div>
    <div class="lsc-build-rejected">Rejected: OmniScript (overkill for a single-screen action)</div>
  </div>

  <!-- Page header (§5.1) -->
  <header class="slds-page-header">...
    Visit · Dr. Reddy — 15 Aug 2026
    <span class="lsc-badge ootb">OOTB</span>
    <button class="slds-button slds-button_brand">
      New Sample Drop <span class="lsc-badge config">Config · Dynamic Action</span>
    </button>
  </header>

  <!-- Path (§5.2) -->
  <div class="slds-path">
    ...
    <span class="lsc-badge ootb">OOTB · Path</span>
  </div>

  <!-- Tabs (§5.3) -->
  <div class="slds-tabs_default">
    ...
    <!-- Samples tab active -->
    <div class="slds-tabs_default__content slds-show">
      <!-- Form for sample drop entry (§5.5) -->
      <div class="slds-grid slds-gutters slds-wrap">
        <div class="slds-col slds-size_1-of-2">
          <div class="slds-form-element">
            <label>HCP</label>
            <input class="slds-input" value="Dr. Anita Reddy" />
            <span class="lsc-badge flow">Flow · licence check</span>
          </div>
        </div>
        <div class="slds-col slds-size_1-of-2">
          <div class="slds-form-element">
            <label>Product & Lot</label>
            <input class="slds-input" value="Cardizex 10 mg · L-2026-088" />
            <span class="lsc-badge ext">Ext · Data Cloud lot feed</span>
          </div>
        </div>
      </div>

      <!-- E-signature card (§5.4 + LWC badge) -->
      <article class="slds-card slds-m-top_medium" style="position: relative;">
        <span class="lsc-badge lwc" style="position: absolute; top: 8px; right: 8px;">LWC · signature pad</span>
        <header class="slds-card__header">
          <h2 class="slds-text-heading_small">HCP e-signature (PDMA)</h2>
        </header>
        <div class="slds-card__body_inner" style="height: 120px;
             background: var(--slds-g-color-surface-2, #f3f3f3);
             border-radius: var(--slds-g-radius-border-2, 0.25rem);">
          <!-- Signature capture area -->
        </div>
      </article>

      <!-- Sample transactions table (§5.6 + Apex badge on Save) -->
      <div class="slds-m-top_medium">
        <h3 class="slds-text-heading_small">Sample transactions this visit</h3>
        <table class="slds-table slds-table_bordered slds-table_cell-buffer">
          ...
        </table>
      </div>

      <!-- Save action (Apex atomic write) -->
      <div class="slds-m-top_medium slds-grid slds-grid_align-end">
        <button class="slds-button slds-button_neutral slds-m-right_x-small">Cancel</button>
        <button class="slds-button slds-button_brand">
          Save Sample Drop <span class="lsc-badge apex">Apex · atomic</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Success state (§5.9) shown after Save -->
  <div class="slds-notify slds-notify_alert slds-theme_success slds-m-around_medium">
    Sample drop saved. 4 units of L-2026-088 decremented. Concur expense entry queued.
    <span class="lsc-badge ext">Ext · Concur</span>
  </div>
</body>
</html>
```

---

## 10. Verification (score-only, no linter)

We do **not** vendor the SLDS Node linter (`slds-linter`). Instead the LLM
runs a lightweight self-check against this primer before saving the
prototype. Every prototype file must open with a header comment recording the
score (score-only rule, per the STEP 6.7 gate-behavior decision).

### The 10-point self-check

Before saving `<Capability>_Prototype.html`, verify:

| # | Check | Passed if… |
|---|-------|-----------|
| 1 | Root token block present | The `:root { --slds-g-* … }` block from §1 is at the top of the `<style>` |
| 2 | No hardcoded colours in body | Every `background:`, `color:`, `border-color:` uses `var(--slds-g-color-*, fallback)` |
| 3 | No hardcoded spacing | Every `padding:`, `margin:` uses either a `--slds-g-spacing-*` hook or an `slds-p-*` / `slds-m-*` utility class |
| 4 | Font sizes use `font-scale-*` or `font-size-base` | No `font-size: 14px`; no invented `font-size-3` / `font-size-4` |
| 5 | Every surface pairs with an on-surface | `background: surface-1` → text uses `on-surface-2` (etc.) |
| 6 | Every colour hook is numbered | No `--slds-g-color-on-surface` without a trailing `-1` / `-2` / `-3` |
| 7 | Every icon has assistive text | Each `<svg>` or icon container has a `<span class="slds-assistive-text">` or `aria-label` |
| 8 | Every interactive element has an LSC badge | Buttons, inputs, cards, action bars carry `.lsc-badge` per §8 |
| 9 | Build-tech banner present | `.lsc-build-banner` opens the prototype below the global header |
| 10 | No dark-mode overrides | Prototype is light-mode only; no `prefers-color-scheme` blocks |

### Score

Write the score as a comment at the very top of the file:

```html
<!--
  LSC Prototype self-check (SLDS 2 + Cosmos primer §10)
  passed: 10 / 10
  notes:  none
-->
```

If any check fails, note it — do **not** block the save. Product owners want
the artifact; a "9/10, note: font-scale-3 used for one badge" is still a
useful review artifact. Matches the score-only rule from §6.7.

---

## 11. What deliberately isn't here

- **Full a11y conformance.** WCAG 2.2 AA gates require the `a11y_expert`
  reviewer. This primer gives a11y basics (assistive text on icons, focus
  outlines from `.slds-input:focus`, no colour-as-sole-indicator) but not a
  verified score.
- **The Node linter.** Score-only, no external tooling.
- **Dark mode.** Every LSC prototype is light-mode only.
- **LWC mechanics.** Signature pads, offline capture, etc. are represented as
  visual placeholders with an `LWC` badge — implementation is not simulated.
- **The full 1,732-icon library.** We ship ~11 LSC-relevant glyphs. Others
  render as an empty box with an `lsc-badge ext` if referenced.

If the story demands any of the above, the story or the prototype request is
out of scope for the primer — escalate to installing the full
`design-quality-experiences` plugin.

---

## 12. Provenance & update policy

- **Source of truth (external):**
  `github.com/salesforce-ux-emu/design-intelligence/packages/skills/applying-slds`
  (SLDS 2 · Cosmos)
  and the published plugin
  `git.soma.salesforce.com/codeai/awesome-context/plugins/design-quality-experiences`.
- **Distilled from these upstream references:**
  - `packages/skills/applying-slds/references/styling-decision-guide.md` (§2, §3, §4 typography)
  - `packages/skills/applying-slds/references/component-selection.md` (§5 blueprint recipes)
  - `packages/skills/applying-slds/references/utilities-quick-ref.md` (§4 utility classes)
  - `packages/skills/applying-slds/SKILL.md` (naming traps, verification pattern)
- **License / visibility:** the upstream skill is `visibility: internal` at
  Salesforce. This primer is a derivative reference for internal use, not a
  redistribution of the plugin.
- **Snapshot date:** 2026-08-08. Refresh when Salesforce ships a new SLDS 2
  major version or when the `applying-slds` skill's version metadata bumps
  above 1.0.
- **Upgrade path:** if the full `design-quality-experiences` plugin is ever
  installed in the workspace (as `.cursor/skills/design-quality-experiences/`
  or `.claude/plugins/design-quality-experiences/`), the LSC Delivery
  Architect can be updated to delegate the prototype rendering to it for a
  verified compliance score. Until then, this primer is the source of truth
  and the STEP 6.7 grounded-prototype contract binds against it.
