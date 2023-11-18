import PyPDF2
with open('Test Resume.pdf','rb') as pdfFile:
    pdfReader = PyPDF2.PdfReader(pdfFile)
    contents = ''
    for page in pdfReader.pages:
        contents += page.extract_text()

print(contents)