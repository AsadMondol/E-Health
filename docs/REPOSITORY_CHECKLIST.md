# Repository publishing checklist

Included: backend scripts, Flask templates/static assets, Custom NER source notebook/configs, annotated training JSON and spaCy training/test files.

Excluded: cloud credentials, credential files, virtual environments, bytecode, checkpoint notebooks, backup copies, raw source dataset documents/spreadsheets, generated uploads/outputs, and trained model weights.

Before public release: review data licensing/permissions for the included annotated dataset; check for sensitive medical text; revoke exposed AWS credentials; inspect git diff/status for secrets; confirm all third-party assets are permitted; select an appropriate license.
