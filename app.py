from flask import Flask, render_template, request, jsonify, send_from_directory, url_for 
from ocr import ParsePDF
from generate_html import HTMLGenerator  # Import HTMLGenerator instead of PDFGenerator
from summarize import TextSummarizer
from speech import TextToSpeechConverter
import os

app = Flask(__name__)

# Global variable to store summarize_dict output
summarize_dict_output = None

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

    global summarize_dict_output
    summarize_dict_output = {
        "title": title,
        "authors": authors,
        "subheadings": subheadings,
        "color_scheme": color_scheme,
        "output_folder": output_folder
    }

    return summarize_dict_output

def process_html(file_path, article_type, summary_type):  # Update function name to reflect HTML generation
    ocr = ParsePDF()
    generation_data = ocr.convert_to_summarize_format(file_path)

    # Constants for article types
    RESEARCH_PAPER = 'Research Paper'
    LEGAL_DOCUMENTS = 'Legal Documents'
    NEWS_ARTICLES = 'News Articles'

    # Constants for summary types
    CONCISE_OVERVIEW = 'Concise Overview'
    DETAILED_OVERVIEW = 'Section-by-Section Analysis'

    # Process the PDF based on article_type and summary_type
    if article_type == RESEARCH_PAPER:
        if summary_type == CONCISE_OVERVIEW:
            # Code for processing Research Paper with Concise Overview
            generation_data = summarize_dict(generation_data)
        elif summary_type == DETAILED_OVERVIEW:
            # Code for processing Research Paper with Section-by-Section Analysis
            generation_data = summarize_dict(generation_data)

    elif article_type == LEGAL_DOCUMENTS:
        # Similar structure for Legal Documents
        if summary_type == CONCISE_OVERVIEW:
            generation_data = summarize_dict(generation_data)
        elif summary_type == DETAILED_OVERVIEW:
            generation_data = summarize_dict(generation_data)

    elif article_type == NEWS_ARTICLES:
        # Similar structure for News Articles
        if summary_type == CONCISE_OVERVIEW:
            generation_data = summarize_dict(generation_data)
        elif summary_type == DETAILED_OVERVIEW:
            generation_data = summarize_dict(generation_data)
    else:
        # Handle unexpected article_type values
        return jsonify({"error": "Invalid article type"})
 
    
    html_generator = HTMLGenerator(  # Use HTMLGenerator instead of PDFGenerator
        title=generation_data['title'],
        authors=generation_data['authors'],
        subheadings=generation_data['subheadings']
    )
    html_generator.generate_html(generation_data)

    return generation_data

def audio_helper():
    global summarize_dict_output

    if summarize_dict_output is not None:
        full_text = ""
        for subheading_data in summarize_dict_output["subheadings"]:
            full_text += f"{subheading_data['subheading']}. {subheading_data['explanation']} "

        # Convert the full text to audio
        converter = TextToSpeechConverter(full_text, output_dir='audio_output', language='en')
        audio_file_path = converter.convert_to_audio(filename='output_audio.mp3')

        return audio_file_path

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the file part is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"})

    file = request.files['file']
    
    # Check if a file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    # Check if article type is selected
    article_type = request.form.get('articleType')
    if not article_type:
        return jsonify({"error": "Article type not selected"})

    # Check if summary type is selected
    summary_type = request.form.get('summaryType')
    if not summary_type:
        return jsonify({"error": "Summary type not selected"})

    try:
        # Save the uploaded PDF file
        file_path = 'uploads/' + file.filename
        file.save(file_path)

        # Process the PDF
        generation_data = process_html(file_path, article_type, summary_type)

        return jsonify({"success": True, "file_path": file_path, "generation_data": generation_data})

    except Exception as e:
        return jsonify({"error": str(e)})

# Route to serve infographic_page.html
@app.route('/infographic')
def serve_infographic():
    return send_from_directory('output', 'infographic_page.html')


@app.route('/play_audio', methods=['POST'])
def play_audio():
    global summarize_dict_output

    if summarize_dict_output is not None:
        audio_file_path = audio_helper()
        if audio_file_path:
            audio_url = url_for('static', filename=os.path.basename(audio_file_path), _external=True)
            return jsonify({"success": True, "audio_url": audio_url})
        else:
            return jsonify({"error": "Failed to convert to audio"})

    return jsonify({"error": "No data to convert"})

if __name__ == '__main__':
    app.run(debug=True, port=8010)
