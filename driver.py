from ocr import ParsePDF
from generate_pdf import PDFGenerator
from summarize import TextSummarizer

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


ocr = ParsePDF()
generation_data = ocr.convert_to_summarize_format('./ocr/parrot.pdf')
generation_data = summarize_dict(generation_data)
pdfmaker = PDFGenerator(title=generation_data['title'], authors=generation_data['authors'], subheadings=generation_data['subheadings'])
pdfmaker.generate_pdf(generation_data)