from flask import Flask, render_template, request, jsonify
from ocr import ParsePDF
from generate_pdf import PDFGenerator
from summarize import TextSummarizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    try:
        # Save the uploaded PDF file
        file_path = 'uploads/' + file.filename
        file.save(file_path)

        # Process the PDF
        generation_data = process_pdf(file_path)

        return jsonify({"success": True, "file_path": file_path, "generation_data": generation_data})

    except Exception as e:
        return jsonify({"error": str(e)})

def process_pdf(file_path):
    ocr = ParsePDF()
    generation_data = ocr.convert_to_summarize_format(file_path)
    generation_data = summarize_dict(generation_data)
    
    pdfmaker = PDFGenerator(
        title=generation_data['title'],
        authors=generation_data['authors'],
        subheadings=generation_data['subheadings']
    )
    pdfmaker.generate_pdf(generation_data)

    return generation_data

def summarize_dict(data_dict):
    title = data_dict.get("title", "Default Title")
    authors = data_dict.get("authors", "Default Authors")
    subheadings = data_dict.get("subheadings", [])
    color_scheme = data_dict.get("color_scheme", "Evening")
    output_folder = data_dict.get("output_folder", "./output")

    summarizer = TextSummarizer()

    for subheading_data in subheadings:
        explanation = subheading_data.get("explanation", "")
        summarized_explanation = summarizer.summarize(explanation)
        subheading_data["explanation"] = summarized_explanation

    return {
        "title": title,
        "authors": authors,
        "subheadings": subheadings,
        "color_scheme": color_scheme,
        "output_folder": output_folder
    }

if __name__ == '__main__':
    app.run(debug=True)
