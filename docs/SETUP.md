# Setup Guide

## Prerequisites
- Python 3.10+ (confirm compatibility with your original spaCy configuration)
- Google Cloud Vision API enabled and Application Default Credentials configured
- AWS account with DynamoDB access; configure AWS credentials using the AWS CLI/profile, environment, or IAM role
- Trained spaCy model directory (not included)
- Microsoft Word on Windows is required by the original `docx2pdf` workflow

## Backend
From the repository root:
```bash
cd backend
python -m venv .venv
# Windows CMD: .venv\Scripts\activate.bat
# PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
mkdir uploads output_files
python flaskrun.py
```

Configure `GOOGLE_APPLICATION_CREDENTIALS` to point to your own Google Cloud service-account file (never commit it). Google Cloud ADC may also be used where supported. Set `FLASK_SECRET_KEY` to a random secret for deployment.

## Custom NER model
The model path is configurable through `SPACY_NER_MODEL`; default is `custom_ner/model-best`. Train using the notebook/configs in `custom_ner/` and place the exported model at the configured path. The original training assets are included, but model weights are not.

## AWS DynamoDB
Set `AWS_REGION` (default `ap-south-1`) and configure credentials through the AWS SDK credential provider chain. Ensure the IAM identity has only the necessary DynamoDB permissions for the `TestingResults` table. The source code can create the table with low provisioned throughput.

## Run the app
Open `http://127.0.0.1:5000`. Upload a supported medical document and follow the classify/review/store flow. The original application workflow uses temporary local files; clear them appropriately and do not process real patient data without approved security and privacy controls.

## Notes
- OCR, docx-to-PDF conversion, and spaCy model loading depend on platform-specific components.
- The source prototype's flow and modules are preserved; this package is not a production-ready deployment.
