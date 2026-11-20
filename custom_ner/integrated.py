import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from google.cloud import vision_v1
from docx import Document
import spacy
import boto3
from botocore.exceptions import NoCredentialsError
import fitz
import os
import io

# Set your Google Cloud Vision API credentials
# Configure Google Cloud Application Default Credentials outside this source file.

# AWS credentials
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')

# Load the trained spaCy NER model from the specified path
MODEL_PATH = os.environ.get('SPACY_NER_MODEL', 'custom_ner/model-best')
nlp = spacy.load(MODEL_PATH)

def extract_handwritten_text(image_path, output_folder):
    client = vision_v1.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = client.document_text_detection(image=image)

    doc = Document()
    docText = response.full_text_annotation.text
    doc.add_paragraph(docText)

    docx_output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(image_path))[0]}.docx")
    doc.save(docx_output_path)
    messagebox.showinfo("Extraction Complete", f"Text extracted and saved as: {docx_output_path}")

def extract_text_from_pdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    extracted_images = []

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_pixmap()

        image_file = os.path.join(output_folder, f'page_{page_number + 1}.png')
        image_list.save(image_file, "png")
        extracted_images.append(image_file)

    return extracted_images

def classify_entities_from_text(text):
    doc = nlp(text)
    diseases = []
    symptoms = []
    medications = []

    for ent in doc.ents:
        if ent.label_ == "DISEASE":
            diseases.append(ent.text)
        elif ent.label_ == "SYMPTOM":
            symptoms.append(ent.text)
        elif ent.label_ == "MEDICATION":
            medications.append(ent.text)

    return diseases, symptoms, medications


# Initialize DynamoDB client with credentials
try:
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
except NoCredentialsError:
    print("AWS credentials not found. Please provide valid credentials.")

def create_table():
    # Define the table schema
    table_schema = {
        'TableName': 'TestingResults',
        'KeySchema': [
            {
                'AttributeName': 'DiseaseName',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'DiseaseName',
                'AttributeType': 'S'  # String
            }
        ],
        # Specify provisioned capacity to stay within Free Tier limits
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    }
    
    # Create the table
    dynamodb.create_table(**table_schema)

def store_test_results(disease_name, symptoms, medication):
    try:
        dynamodb.describe_table(TableName='TestingResults')
    except dynamodb.exceptions.ResourceNotFoundException:
        create_table()

    dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)

    table = dynamodb_resource.Table('TestingResults')

    item = {
        'DiseaseName': disease_name,
        'Symptoms': symptoms,
        'Medication': medication
    }

    table.put_item(Item=item)
    messagebox.showinfo("Results Stored", "Test results stored successfully.")

def browse_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        txt_path = extract_text_from_pdf(pdf_path, output_folder)
        messagebox.showinfo("PDF Extracted", f"PDF text extracted and saved as: {txt_path}")

def classify_entities():
    with open(output_docx, 'rb') as file:
        combined_text = Document(file).text

    diseases, symptoms, medications = classify_entities_from_text(combined_text)

    for disease in diseases:
        store_test_results(disease, symptoms, medications)

# Create the main window
root = tk.Tk()
root.title("E-Health Application")

# Add widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

browse_btn = tk.Button(frame, text="Browse PDF", command=browse_pdf)
browse_btn.grid(row=0, column=0, padx=5, pady=5)

classify_btn = tk.Button(frame, text="Classify Entities", command=classify_entities)
classify_btn.grid(row=0, column=1, padx=5, pady=5)

# Run the application
root.mainloop()

input_folder = r'C:\Users\USER\Desktop\E-Health\Custom_NER\input\demo.pdf'
output_folder = r'C:\Users\USER\Desktop\E-Health\Custom_NER\output_images'
output_docx = r'C:\Users\USER\Desktop\E-Health\Custom_NER\output_docx\combined_output.docx'
