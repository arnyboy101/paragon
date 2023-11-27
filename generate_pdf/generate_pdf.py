import tkinter as tk
from tkinter import ttk, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from tkinter import Tk, Label, Button, StringVar, OptionMenu
from functools import partial
import textwrap

class PDFGenerator:
    def __init__(self, title, authors, subheadings):
        self.title = title
        self.authors = authors
        self.subheadings = subheadings

    def create_infographic(self, pdf_file, color_scheme="Evening"):
        # Create a PDF document
        canvas = Canvas(pdf_file, pagesize=letter)

        # Set background and box colors based on the selected color scheme
        color_schemes = {
            "Evening": ("#c7cafc", "#5861fc"),
            "Lime": ("#c5fcd4", "#0afa4a"),
            "Miami": ("#fce1fc", "#f502ed"),
            "Founder's Fav": ("#b9f0db", "#04b876")
        }

        if color_scheme not in color_schemes:
            raise ValueError("Invalid color scheme")

        background_color, box_color = color_schemes[color_scheme]

        # Set background color
        canvas.setFillColor(colors.HexColor(background_color))
        canvas.rect(0, 0, letter[0], letter[1], fill=True)

        # Set fonts
        title_font = "Times-Bold"
        text_font = "Helvetica"

        # Calculate the width of the title and authors
        title_width = canvas.stringWidth(self.title, title_font, 16)
        authors_width = canvas.stringWidth("Authors: " + self.authors, title_font, 12)

        # Center the title and authors
        title_x = (letter[0] - title_width) / 2
        authors_x = (letter[0] - authors_width) / 2

        # Set title and authors with Times New Roman font
        canvas.setFont(title_font, 16)
        canvas.setFillColorRGB(0, 0, 0)  # Black color
        canvas.drawString(title_x, 750, self.title)

        canvas.setFont(title_font, 12)  # Use the same font for Authors
        canvas.drawString(authors_x, 730, "Authors: " + self.authors)

        # Set box and text parameters
        initial_box_width = 400
        box_height = 60
        box_margin = 20
        text_margin = 20

        # Draw boxes and text for each subheading
        # Draw boxes and text for each subheading
        y_position = 700
        for subheading_data in self.subheadings:
            explanation_lines = self.wrap_text(subheading_data["explanation"], text_font, 8, initial_box_width - 2 * text_margin, canvas)
            total_lines = len(explanation_lines)
            required_box_height = self.calculate_required_box_height(initial_box_width, box_height, text_margin, total_lines)

            # Check if there is enough space on the page
            if y_position - required_box_height < 50:
                # Move to a new page
                canvas.showPage()
                y_position = 750  # Reset y_position for the new page
                # Set background color for the new page
                canvas.setFillColor(colors.HexColor(background_color))
                canvas.rect(0, 0, letter[0], letter[1], fill=True)

            # Draw box
            canvas.setFillColor(box_color)
            canvas.setStrokeColor(box_color)
            canvas.roundRect(100, y_position, initial_box_width, -required_box_height, 5, fill=True)

            
            sub_heading_y = y_position - 20

            # Draw text
            canvas.setFillColor(colors.black)  # Set text color to black
            canvas.setFont("Helvetica-Bold", 12)  # Use bold font for sub-heading
            canvas.drawString(100 + text_margin, sub_heading_y, subheading_data["subheading"])

            # Draw explanation text inside the box with wrapping
            canvas.setFont("Helvetica", 8)
            explanation_text = "\n".join(explanation_lines)

            text_obj = canvas.beginText(100 + text_margin, sub_heading_y - text_margin)
            text_obj.textLines(explanation_text)
            canvas.drawText(text_obj)

            # Move to the next position
            y_position -= required_box_height + box_margin

        # Save the PDF
        canvas.save()

    def calculate_required_box_height(self, box_width, box_height, text_margin, total_lines):
        return box_height + (total_lines - 1) * (8 + text_margin) if total_lines > 1 else box_height

    def wrap_text(self, text, font, font_size, max_width, canvas):
        lines = []
        for para in text.split("\n"):
            lines.extend(self.wrap_line(para, font, font_size, max_width, canvas))
        return lines

    def wrap_line(self, text, font, font_size, max_width, canvas):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            width = canvas.stringWidth(current_line + word, font, font_size)
            if width > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line += " " + word

        if current_line:
            lines.append(current_line)

        return lines


class PDFGeneratorApp:
    def __init__(self):
        self.title = "Research Paper Title"
        self.authors = "John Doe, Jane Smith"
        self.subheadings = [
            {"subheading": "Introduction", "explanation": "This section provides an overview of the research."},
            {"subheading": "Methodology", "explanation": "The study concludes with a summary of findings and potential implications. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI"},
            {"subheading": "Results", "explanation": "The study concludes with a summary of findings and potential implications. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI"},
            {"subheading": "Conclusion", "explanation": "The study concludes with a summary of findings and potential implications. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI. Happiness is the birth of AI"},
            {"subheading": "Comparative Analysis", "explanation": "The results of the research are presented and analyzed."},
            {"subheading": "Keywords", "explanation": "The study concludes with a summary of findings and potential implications."}
        ]

    def generate_pdf(self, theme_var, root):
        color_scheme = theme_var.get()
        pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_file:
            pdf_generator = PDFGenerator(self.title, self.authors, self.subheadings)
            pdf_generator.create_infographic(pdf_file, color_scheme)
            root.destroy()  # Close the Tkinter UI

    def create_ui(self):
        root = Tk()
        root.title("PDF Generator")

        theme_var = StringVar(root)
        themes = ["Evening", "Lime", "Miami", "Founder's Fav"]
        theme_var.set(themes[0])

        generate_pdf_partial = partial(self.generate_pdf, theme_var, root)

        Label(root, text="Select Theme:").grid(row=0, column=0, padx=10, pady=10)
        theme_menu = OptionMenu(root, theme_var, *themes)
        theme_menu.grid(row=0, column=1, padx=10, pady=10)

        generate_button = Button(root, text="Generate PDF", command=generate_pdf_partial)
        generate_button.grid(row=1, column=0, columnspan=2, pady=20)

        root.mainloop()


if __name__ == "__main__":
    pdf_generator_app = PDFGeneratorApp()
    pdf_generator_app.create_ui()
