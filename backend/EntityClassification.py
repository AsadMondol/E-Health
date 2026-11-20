import spacy
import fitz

# Load the trained spaCy NER model from the specified path
MODEL_PATH = os.environ.get('SPACY_NER_MODEL', 'custom_ner/model-best')
nlp = spacy.load(MODEL_PATH)

def classify_entities_from_text(text):
    doc = nlp(text)
    entities = {'diseases': [], 'symptoms': [], 'medications': []}
    
    # Iterate through recognized entities and classify them
    for ent in doc.ents:
        print(f"Recognized entity: {ent.text}, Label: {ent.label_}")  # Debug print
        if ent.label_ == 'DISEASE':
            entities['diseases'].append(ent.text)
        elif ent.label_ == 'SYMPTOM' or ent.label_ == 'SYMPTOMS':  # Add 'SYMPTOMS' for safety
            entities['symptoms'].append(ent.text)
        elif ent.label_ == 'MEDICATION':
            entities['medications'].append(ent.text)
    
    print(f"Classified entities: {entities}")  # Debug print
    return entities

def classify_entities_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    print(f"Extracted text: {text[:500]}...")  # Debug print (showing the first 500 characters)
    entities = classify_entities_from_text(text)
    return entities
