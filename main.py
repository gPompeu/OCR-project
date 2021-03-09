import cv2
import pytesseract

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

import subprocess

def main():
    file_path = filedialog.askopenfilename(
        title = 'Selecione o PDF que deseja converter para texto',
        filetypes = [('Arquivos PDF', '.pdf')],
    )
    
    if file_path:
        images = convert_from_path(file_path)
        
        # output_text = ''

        # for image in images:
        #     output_text += pytesseract.image_to_string(image)

        # print(output_text)
        # with open('texto_do_pdf.txt', 'w') as output_file:
            # output_file.write(output_text)
        print(pytesseract.image_to_string(images[0]))
        input("\n[Enter] para fechar")

if __name__ == '__main__':
    main()