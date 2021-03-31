import pytesseract

popplerPath = './poppler/Library/bin'
tesseractPath = './tesseract/tesseract'

def setTesseractPath():
    pytesseract.pytesseract.tesseract_cmd = tesseractPath