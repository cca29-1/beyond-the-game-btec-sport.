# Microsoft Lists → BTEC hub

## Mapping contract

Use your existing List where possible. These are **proposed display names**, not recovered original internal column names. In Power Automate choose the corresponding dynamic values from your actual List; SharePoint internal names may differ after renaming columns. The hub reads the JSON names on the right, never Microsoft Lists directly.

| Suggested Lists column | Column type / rule | Published JSON |
| --- | --- | --- |
| Title | Single line of text, required | `title` |
| Course | Choice; use exactly `BTEC Sport` | Filter before export |
| Unit | Number, no decimal places; Pearson unit ID | `unit` (integer) |
| LearningAim | Choice with multiple selections; e.g. A, B, C | `learningAims` (array of strings) |
| ResourceType | Choice; e.g. Lesson, Revision, Video, Worksheet | `type` |
| ResourceURL | Hyperlink; required | `url` (URL string, not display text/object) |
| Description | Plain text, multiple lines | `description` |
| Tags | Single line of text, semicolon separated | `tags` (array of strings) |
| Published | Yes/No; default No | Filter for true before export |

For an existing Unit choice such as `Unit 1`, transform it to integer `1`; do not send a unit title to the number field. If using multi-choice fields, inspect a real **Get items** result: connector outputs can be string arrays or objects with a `Value` property. Map those to plain strings. Do not send a string containing `["A"]`, a semicolon string or a SharePoint multi-choice wrapper as `learningAims`. For a blank LearningAim or Tags value output `[]`. Trim tag values and remove empty values after splitting on `;`. Use plain text for Description because the hub displays text rather than HTML.

If you share a List with the A Level hub, both flows must filter their own Course value. This workflow must target only `cca29-1/beyond-the-game-btec-sport` and event `btec-resources-updated`. A separate BTEC List is also supported. Never export assessment marks, learner details, credentials, draft assignments or other fields beyond this resource catalogue.

## Power Automate flow

This package includes the receiving GitHub workflow, not a pre-authenticated Power Automate flow. Your tenant connections, List and column internal names must be selected in Power Automate. The HTTP action can require a premium licence and must comply with your tenant's connector policy.

1. Create a **scheduled cloud flow** (for example every 30 minutes). A full scheduled snapshot also catches deletions and unpublishing. If you add a created/modified trigger for quicker updates, keep periodic reconciliation for deletions.
2. Set trigger concurrency to **1** to avoid overlapping exports.
3. Add SharePoint **Get items** for the correct site and List. Enable pagination and set a threshold sufficient for the complete List. If the List grows beyond the chosen threshold/service limit, implement paging before relying on this flow. A partial snapshot would remove omitted entries from the hub.
4. Filter to Course exactly `BTEC Sport` and Published true. You may use **Filter array** after Get items; alternatively use an OData filter with your actual internal names. For an exact choice match and Yes/No column, a typical filter is `Course eq 'BTEC Sport' and Published eq 1`; adjust it to your own schema.
5. Add **Select** to map only the retained records to the JSON shape below. Convert Unit to an integer. Turn multi-choice aims and semicolon tags into arrays as described above. Use URL-only text from ResourceURL; inspect output if the connector returns a hyperlink object.
6. Add an HTTP **POST** action using the GitHub details below. The request body must contain the actual Select array as `resources`, not a quoted JSON string.
7. Test with one published BTEC row, one unpublished BTEC row and one A Level row. Only the published BTEC row should appear. Test multiple aims, a deletion and unpublishing, then confirm a student can open the resource link.
8. Configure flow failure notifications. Inspect GitHub Actions after testing: dispatch acceptance does not guarantee that validation, commit or deployment succeeded.

### Request

URL:

```text
https://api.github.com/repos/cca29-1/beyond-the-game-btec-sport/dispatches
```

Headers:

```text
Accept: application/vnd.github+json
Authorization: Bearer YOUR_REPOSITORY_SCOPED_TOKEN
X-GitHub-Api-Version: 2022-11-28
Content-Type: application/json
```

Create a fine-grained GitHub token limited to the BTEC repository with **Contents: Read and write**, or use an organisation-approved GitHub App. Store it in an approved secret store/secured flow configuration. Enable secure inputs and outputs on actions handling it; never paste a live token into a shared flow export, this repository or the browser. Rotate it before expiry.

Body example (replace the sample record with the entire output array from Select):

```json
{
  "event_type": "btec-resources-updated",
  "client_payload": {
    "resources": [
      {
        "course": "BTEC Sport",
        "published": true,
        "unit": 1,
        "title": "Anatomy revision guide",
        "url": "https://your-school.sharepoint.com/path-to-resource",
        "description": "Review key terms.",
        "learningAims": ["A", "B"],
        "type": "Revision",
        "tags": ["anatomy", "revision"]
      }
    ],
    "allowEmpty": false
  }
}
```

In the flow, insert the **Body output of Select** as the value of `resources` using dynamic content/expression mode. Check the HTTP action's resolved test input to confirm this is an array. In expression form that value is typically `body('Select')`, where `Select` must match your action name.

Every request is a **complete replacement snapshot**, not a single-row update. Missing rows are removed. A zero-row replacement is rejected by default to guard against a broken query clearing the catalogue. If you deliberately remove/unpublish every resource, send `resources: []` with `allowEmpty: true`; the initial supplied empty catalogue can be deployed manually without that flag. Keep automatic empty replacements disabled until you have tested your filtering and deletion policy.

The workflow checks optional `course` and `published` markers, strips them from the saved public JSON, and validates required fields. Include those markers in Lists exports as an extra cross-hub check. It cannot independently authenticate a row's original Microsoft source; correct flow filtering remains essential.

GitHub limits dispatch payload size (under 64 KB) and the number of top-level client payload properties. This structure has two properties. If a complete catalogue approaches the limit, use an approved authenticated process to commit `resources.json` directly or introduce a server-side integration; do not split one snapshot into several replacement dispatches.

## Sources

- [SharePoint Get items / Get files guidance and pagination](https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files)
- [Power Automate data operations including Select and Filter array](https://learn.microsoft.com/en-us/power-automate/data-operations)
- [GitHub repository dispatch API, permissions and payload requirements](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
