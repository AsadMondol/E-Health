# Security and Privacy

- Medical documents and OCR text can contain sensitive personal health information. Do not commit real patient files or identifiable datasets.
- Never commit Google Cloud service-account JSON, AWS access keys, `.env`, secrets, or credentials.
- The original source contained hard-coded AWS keys and a hard-coded Google credentials path. Those have been removed in this curated package. **Revoke/rotate the exposed AWS key immediately.**
- Use Google Application Default Credentials or a local credential file referenced through `GOOGLE_APPLICATION_CREDENTIALS`.
- Use AWS SDK credential profiles, environment configuration, or IAM roles—not embedded credentials.
- Set a strong `FLASK_SECRET_KEY`; do not use the development fallback in production.
- Restrict AWS IAM permissions, Google Vision permissions, file upload types/sizes, access to stored records, and retention periods.
- Add authentication, authorization, CSRF protection, secure file handling, and deployment hardening before production.
