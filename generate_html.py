class HTMLGenerator:
    def __init__(self, title, authors, subheadings):
        self.title = title
        self.authors = authors
        self.subheadings = subheadings

    def generate_html(self, data_dict):
        title = data_dict.get("title", "Default Title")
        authors = data_dict.get("authors", "Default Authors")
        subheadings = data_dict.get("subheadings", [])

        output_folder = data_dict.get("output_folder", ".")
        color_scheme = data_dict.get("color_scheme", "Evening")

        html_file = f"{output_folder}/{title.replace(' ', '_')}_infographic.html"
        html_generator = HTMLGenerator(title, authors, subheadings)
        html_content = html_generator.create_infographic(color_scheme)

        with open(html_file, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    def create_infographic(self, color_scheme="Evening"):
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

        # Build HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    background-color: {background_color};
                    font-family: 'Helvetica', sans-serif;
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-around;
                }}
                .header {{
                    background-color: {box_color};
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                    width: 100%;
                    box-sizing: border-box;
                }}
                .title {{
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .authors {{
                    font-size: 14px;
                }}
                .box {{
                    background-color: {box_color};
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px;
                    width: calc(25% - 20px);  /* 25% width with 20px margin on each side */
                    box-sizing: border-box;
                    cursor: pointer; /* Add cursor pointer to indicate clickability */
                }}
                .subheading {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .explanation {{
                    font-size: 12px;
                    display: none; /* Initially hide explanations */
                }}
            </style>
            <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
            <script>
                $(document).ready(function() {{
                    $(".box").click(function() {{
                        $(this).find(".explanation").slideToggle();
                    }});
                }});
            </script>
            <title>{self.title} Infographic</title>
        </head>
        <body>
            <div class="header">
                <div class="title">{self.title}</div>
                <div class="authors">Authors: {self.authors}</div>
            </div>
        """

        # Add subheadings to HTML content
        for subheading_data in self.subheadings:
            explanation_lines = self.wrap_text(subheading_data["explanation"], 8, 400 - 2 * 20)
            explanation_text = "<br>".join(explanation_lines)

            html_content += f"""
            <div class="box">
                <div class="subheading">{subheading_data["subheading"]}</div>
                <div class="explanation">{explanation_text}</div>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        return html_content


    def wrap_text(self, text, font_size, max_width):
        lines = []
        current_line = ""

        for para in text.split("\n"):
            words = para.split()
            for word in words:
                width = len(current_line) + len(word) * font_size
                if width > max_width:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line += " " + word

            if current_line:
                lines.append(current_line)

        return lines