import scipdf

class ParsePDF:
    def __init__(self):
        pass

    def parse_pdf_to_dict(self, pdf_file, output_folder=None):
        article_dict = scipdf.parse_pdf_to_dict(pdf_file)
        if output_folder:
            print(f"Output folder specified: {output_folder}")
        return article_dict

    def parse_figures(self, pdf_folder, output_folder=None):
        if output_folder:
            print(f"Output folder specified: {output_folder}")
        scipdf.parse_figures(pdf_folder, output_folder=output_folder)

    def convert_to_summarize_format(self, pdf_file):
        article_dict = self.parse_pdf_to_dict(pdf_file)
        
        title = article_dict.get("title", "Default Title")
        authors = article_dict.get("authors", "Default Authors")
        
        subheadings = []
        for section in article_dict.get("sections", []):
            subheading_data = {
                "subheading": section.get("heading", ""),
                "explanation": section.get("text", "")
            }
            subheadings.append(subheading_data)

        return {
            "title": title,
            "authors": authors,
            "subheadings": subheadings,
            "color_scheme": "Evening",
            "output_folder": "./output"
        }