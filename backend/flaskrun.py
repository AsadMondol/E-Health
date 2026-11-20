from flask import Flask, flash, render_template, request, redirect, url_for
import os
import textExtraction
import EntityClassification
import wareHouse

app = Flask(__name__)

# Set the secret key to a random bytes value
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-only-change-me')  # Set FLASK_SECRET_KEY before deployment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['pdfFile']
        if file.filename == '':
            return render_template('index.html', message='No file selected')
        os.makedirs('uploads', exist_ok=True)
        filename = os.path.join('uploads', file.filename)
        file.save(filename)
        output_folder = 'output_files'
        try:
            processed_file, extracted_text = textExtraction.process_file(filename, output_folder)
            return redirect(url_for('classify'))
        except Exception as e:
            return f"Error processing file: {e}"

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        try:
            entities = EntityClassification.classify_entities_from_pdf('output_files/combined_output.pdf')
            print(f"Entities passed to template: {entities}")  # Debug print
            return render_template('storedata.html', entities=entities)
        except Exception as e:
            return f"Error classifying entities: {e}"
    else:
        return render_template('classify.html')



@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':
        disease_name = request.form.get('disease_name')
        symptoms = request.form.getlist('symptoms')
        medication = request.form.getlist('medication')

        # Debugging: print the form data
        print(f"disease_name: {disease_name}, symptoms: {symptoms}, medication: {medication}")

        if not disease_name:
            return render_template('storedata.html', message='Disease name is required', entities={'diseases': [], 'symptoms': symptoms, 'medications': medication})

        try:
            wareHouse.store_test_results(disease_name, symptoms, medication)
            flash('Entities stored into warehouse successfully!')
        except Exception as e:
            return f"Error storing test results: {e}"
        
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
