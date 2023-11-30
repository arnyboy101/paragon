import scipdf
article_dict = scipdf.parse_pdf_to_dict('article.pdf') # return dictionary
print(article_dict)

scipdf.parse_figures('sample.pdf', output_folder='figures') # folder should contain only PDF files