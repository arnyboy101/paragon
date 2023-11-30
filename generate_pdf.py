from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from functools import partial

class PDFGenerator:
    def __init__(self, title, authors, subheadings):
        self.title = title
        self.authors = authors
        self.subheadings = subheadings

    def generate_pdf(self, data_dict):
        title = data_dict.get("title", "Default Title")
        authors = data_dict.get("authors", "Default Authors")
        subheadings = data_dict.get("subheadings", [])

        output_folder = data_dict.get("output_folder", ".")
        color_scheme = data_dict.get("color_scheme", "Evening")

        pdf_file = f"{output_folder}/{title.replace(' ', '_')}_infographic.pdf"
        pdf_generator = PDFGenerator(title, authors, subheadings)
        pdf_generator.create_infographic(pdf_file, color_scheme)

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