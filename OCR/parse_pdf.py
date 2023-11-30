import scipdf
article_dict = scipdf.parse_pdf_to_dict('article.pdf') # return dictionary
print(article_dict.keys())

scipdf.parse_figures('article.pdf', output_folder='figures') # folder should contain only PDF files