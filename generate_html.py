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
        html_content = self.create_infographic(color_scheme)

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

        # You can directly assign the new colors here if they are not part of a selectable scheme
        background_color = "#C2A384"
        box_color = "#D89F67"

        # Build HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    background-color: {background_color}; /* Updated background color */
                    font-family: 'Helvetica', sans-serif;
                    color: #333; /* Assuming you want a darker color for the text */
                    padding: 20px;
                }}
                .title {{
                    text-align: center;
                    font-family: 'Times New Roman', serif;
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 0.5em; /* Add some space below the title */
                }}
                .authors {{
                    text-align: center;
                    font-family: 'Arial', sans-serif;
                    font-size: 20px;
                    margin-bottom: 2em; /* Add some space below the authors */
                }}
                .card-container {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-wrap: wrap;
                    margin: 20px;
                }}
                .card {{
                    background-color: {box_color};
                    border-radius: 5px;
                    padding: 20px;
                    margin: 10px;
                    width: 45%;  /* 45% width with 10px margin on each side */
                    box-sizing: border-box;
                    cursor: pointer; /* Add cursor pointer to indicate clickability */
                }}
                .subheading {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .explanation {{
                    font-size: 14px;
                }}
            </style>
            <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
            <script>
                $(document).ready(function() {{
                    var currentCard = 0;
                    var totalCards = $(".card").length;

                    $(".card").hide();
                    $(".card").eq(currentCard).show();

                    updateButtonVisibility(); // Call on page load to initialize the counter

                    $("#nextButton").click(function() {{
                        if (currentCard < totalCards - 1) {{
                            $(".card").eq(currentCard).hide();
                            currentCard++;
                            $(".card").eq(currentCard).show();
                            updateButtonVisibility();
                        }}
                    }});

                    $("#prevButton").click(function() {{
                        if (currentCard > 0) {{
                            $(".card").eq(currentCard).hide();
                            currentCard--;
                            $(".card").eq(currentCard).show();
                            updateButtonVisibility();
                        }}
                    }});

                    function updateButtonVisibility() {{
                        $("#prevButton").toggle(currentCard > 0);
                        $("#nextButton").toggle(currentCard < totalCards - 1);
                        $("#cardCounter").text((currentCard + 1) + " of " + totalCards); // Update the counter text
                    }}

                }});
        </script>

        <title>{self.title} Infographic</title>
        </head>
        <body>
            <div class="title">{self.title}</div>
            <div class="authors">Authors: {self.authors}</div>
            <div class="card-container">
        """

        # Add subheadings to HTML content
        for subheading_data in self.subheadings:
            explanation_lines = self.wrap_text(subheading_data["explanation"], 14, 400 - 2 * 20)
            explanation_text = "<br>".join(explanation_lines)

            html_content += f"""
            <div class="card">
                <div class="subheading">{subheading_data["subheading"]}</div>
                <div class="explanation">{explanation_text}</div>
            </div>
            """

        html_content += """
            </div>
            <div style="text-align: center; margin-top: 10px;">
                <button id="prevButton">Previous</button>
                <button id="nextButton">Next</button>
            </div>
            <div id="cardCounter" style="text-align: center; margin-top: 5px;"></div> <!-- Card counter display -->
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
