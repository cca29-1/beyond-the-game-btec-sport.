# Beyond the Game — BTEC Sport starter

Prepared exclusively for **cca29-1/beyond-the-game-btec-sport**.

## What is included

- `index.html`: responsive 14-unit learning hub, text search, unit, learning aim/content area and resource type filters; keyboard access; clear filters; loading/error/empty states.
- `units.json`: editable unit menu.
- `resources.json`: intentionally empty (`[]`). No sample resources are published.
- `.github/workflows/publish-resources.yml`: validate, optionally save a Microsoft Lists snapshot, then publish the three website files using GitHub Pages.
- `scripts/prepare_resources.py`: rejects malformed records and unsafe links before publishing.
- `MICROSOFT-LISTS-SETUP.md`: mapping and Power Automate integration.

## Reconstruction assumptions

The referenced chat's actual assistant replies could not be retrieved. Exact previously agreed column names, branding and chosen 14 units therefore could not be recovered. This starter uses a documented mapping that can be adapted without changing the hub. It defaults to **units 1–14 from Pearson BTEC Nationals Sport (2016)**, not a claim that every BTEC Sport course teaches those 14. If your programme uses a different selection, edit `units.json` before connecting Lists. Keep Pearson unit IDs rather than renumbering optional units. Learning aim labels are populated from your resources instead of inventing assessment content; externally assessed units can use their content area letters.

Unit source: [Pearson Sport specification](https://qualifications.pearson.com/content/dam/pdf/BTEC-Nationals/Sport/20161/specification-and-sample-assessments/btec-l3-national-ext-dip-in-sport-spec.pdf). Confirm your centre's specification and delivery plan.

## 1. Upload to the BTEC repository

1. Extract the ZIP and open its `beyond-the-game-btec-sport` folder.
2. In [the BTEC repository](https://github.com/cca29-1/beyond-the-game-btec-sport), add the contents at the repository root on `main`. Do not upload the ZIP itself or add an extra enclosing folder. Include the hidden `.github` folder; create `.github/workflows/publish-resources.yml` through GitHub's **Add file → Create new file** if your upload omits it.
3. Confirm the repository contains `index.html`, `resources.json`, `units.json`, `README.md`, `MICROSOFT-LISTS-SETUP.md`, `scripts/prepare_resources.py` and `.github/workflows/publish-resources.yml`.
4. Keep all files, workflow tokens and automation destinations separate from the A Level hub. No changes to the A Level repository are required.

## 2. Enable publishing

A private repository requires an eligible GitHub plan for Pages. A private repository does **not** automatically make its Pages website private. Decide whether the resource catalogue may be public before enabling Pages; Microsoft/SharePoint resource permissions remain separate. For confidential catalogues, use hosting with authentication or an eligible GitHub Enterprise Pages access-control setup.

1. Repository **Settings → Pages → Build and deployment → Source → GitHub Actions**.
2. Under **Settings → Actions → General**, allow the actions used here. Repository policies must permit workflow writes if Lists snapshots will be committed; branch protection may also need an approved automation path.
3. Open **Actions → Publish BTEC Sport resources → Run workflow** on `main`.
4. Open the website URL reported by the successful deployment. The usual project URL is `https://cca29-1.github.io/beyond-the-game-btec-sport/`, subject to your Pages configuration. It is not live until you enable and run publishing.
5. Expect all 14 unit cards and a friendly empty-resource message on the initial deployment.

Official guidance: [publishing sources and private repository plan support](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## 3. Add resources

Either edit `resources.json` directly and commit to `main`, or connect Microsoft Lists using `MICROSOFT-LISTS-SETUP.md`. Each resource uses this shape (example only; the supplied file stays empty):

```json
[
  {
    "unit": 1,
    "title": "Anatomy revision guide",
    "url": "https://your-school.sharepoint.com/path-to-resource",
    "description": "Revise key terms before the next lesson.",
    "learningAims": ["A"],
    "type": "Revision",
    "tags": ["anatomy", "revision"]
  }
]
```

Use real school-approved URLs. `unit` must be a number matching an ID in `units.json`. `learningAims` and `tags` are arrays of strings; use `[]` for a whole-unit resource or no tags. Use consistent aim codes such as `A`, `B`, `C` and consistent type names. Filters use exact labels. Unit selection narrows the aim/type choices. The aim filter is based on available resources and will initially be empty.

## Preview and checks

From the extracted folder, run `python3 -m http.server 8000`, then open `http://localhost:8000`. Opening the HTML directly as a file can block JSON loading.

Run `python3 scripts/prepare_resources.py` to validate the local catalogue. Before publishing actual resources, check unit filtering, a multi-aim resource, search, clear filters, a no-match result, mobile layout and a Microsoft link as a student. Resource links open in a new tab and retain the source system's permissions.

## Troubleshooting

- **Pages unavailable:** check your private repository's plan eligibility and organisation policy.
- **404:** verify Pages source, completed Actions deployment, branch `main` and root-level website files.
- **Hub load error:** check `units.json` and `resources.json` exist beside `index.html` and contain valid JSON.
- **Dispatch returns 204 but no update:** inspect Actions; 204 accepts the event, it does not confirm a successful deployment.
- **Push rejected:** branch protection or policy blocks the workflow's snapshot commit. Use an organisation-approved GitHub App or direct reviewed JSON edits instead of weakening protections blindly.
- **New list entry missing:** check course/publication filters, pagination, mapping and the latest flow/workflow run.
- **Link access denied:** grant the intended students access in Microsoft 365. The hub cannot override SharePoint permissions.

No GitHub or Microsoft credentials belong in website files. Only the three runtime website files are uploaded to Pages. This package has not been pushed to GitHub or connected to your Microsoft tenant.
