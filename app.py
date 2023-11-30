from flask import Flask, render_template, request, jsonify
from ocr import ParsePDF
from generate_pdf import PDFGenerator
from summarize import TextSummarizer
from speech import TextToSpeechConverter  # Import the TextToSpeechConverter class

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

@app.route('/play_audio', methods=['POST'])
def play_audio():
    global summarize_dict_output

    if summarize_dict_output is not None:
        audio_file_path = audio_helper()

        if audio_file_path is not None:
            return jsonify({"success": True, "audio_file_path": audio_file_path})
        else:
            return jsonify({"error": "Failed to convert to audio"})

    return jsonify({"error": "No data to convert"})

if __name__ == '__main__':
    app.run(debug=True, port=8009)
