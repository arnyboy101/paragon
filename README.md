# paragon
## Instructions
Type ```pip3 install -r requirements.txt``` after creating a virtual environemnt to run the generate PDF model. \\
These are the other installs you need to run - \\
```
pip install git+https://github.com/titipata/scipdf_parser 
```  
\\
```python -m spacy download en_core_web_sm```

For the PDF parser to work you need this docker container to be running locally - 
``` docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0 ``` \\
For the pdf to be uploaded successfully, please create the following directories in the paragon directory - \\
```mkdir uploads``` \\
```mkdir output```

