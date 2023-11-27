from generate_pdf import PDFGeneratorApp

# Define your data
title = "Research Paper Title"
authors = "John Doe, Jane Smith"
subheadings = [
    {"subheading": "Introduction", "explanation": "This section provides an overview of the research."},
    {"subheading": "Methodology", "explanation": "The study concludes with a summary of findings and potential implications. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI"},
    # Add more subheadings as needed
]

# Create an instance of PDFGeneratorApp and feed the data
pdf_generator_app = PDFGeneratorApp(title, authors, subheadings)
pdf_generator_app.create_ui()
