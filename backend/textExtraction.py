# textExtraction.py
import os
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import fitz
from docx2pdf import convert

# Configure Google Cloud Application Default Credentials outside this source file.

def extract_handwritten_text_and_save_as_docx(image_path, output_folder):
    client = vision_v1.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = client.document_text_detection(image=image)

    doc = Document()
    docText = response.full_text_annotation.text

    # Add and format text
    paragraph = doc.add_paragraph(docText)
    for run in paragraph.runs:
        run.font.size = Pt(12)  # Set font size
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY  # Set text alignment

    docx_output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(image_path))[0]}.docx")
    doc.save(docx_output_path)
    print(f"Extracted text saved as a DOCX file: {docx_output_path}")
    return docx_output_path, docText

def extract_pages_from_pdf(input_file, output_dir):
    pdf_document = fitz.open(input_file)
    extracted_images = []
    os.makedirs(output_dir, exist_ok=True)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_pixmap()

        image_file = os.path.join(output_dir, f'page_{page_number + 1}.png')
        image_list.save(image_file)
        extracted_images.append(image_file)

    return extracted_images

def combine_docs_to_single_docx(input_dir, output_file):
    doc = Document()
    docx_files = [filename for filename in os.listdir(input_dir) if filename.lower().endswith('.docx')]

    for filename in sorted(docx_files):
        file_path = os.path.join(input_dir, filename)
        sub_doc = Document(file_path)
        for element in sub_doc.element.body:
            doc.element.body.append(element)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(12)  # Set font size
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY  # Set text alignment

    doc.save(output_file)
    print(f"Combined DOCX file saved as: {output_file}")

def process_file(input_file, output_folder):
    if input_file.lower().endswith('.pdf'):
        image_files = extract_pages_from_pdf(input_file, output_folder)
    else:
        image_files = [input_file]

    os.makedirs(output_folder, exist_ok=True)

    extracted_docs = []
    all_extracted_text = ""
    for image_path in image_files:
        docx_file, extracted_text = extract_handwritten_text_and_save_as_docx(image_path, output_folder)
        extracted_docs.append(docx_file)
        all_extracted_text += extracted_text + "\n"

    output_docx = os.path.join(output_folder, 'combined_output.docx')
    combine_docs_to_single_docx(output_folder, output_docx)
    
    # Convert the combined DOCX file to PDF
    output_pdf = os.path.join(output_folder, 'combined_output.pdf')
    convert(output_docx, output_pdf)
    print(f"Combined PDF file saved as: {output_pdf}")
    return output_pdf, all_extracted_text
