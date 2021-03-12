import pytesseract
import os
from time import sleep
from tkinter import filedialog, Tk
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from re import compile
from tempfile import TemporaryDirectory

def main():

    root = Tk()
    root.withdraw()

    reg_exp = compile(r'\s\d{7}\s')
    poppler_path = r'.\poppler\Library\bin'
    pytesseract.pytesseract.tesseract_cmd = r'.\tesseract\tesseract'

    folder_path = filedialog.askdirectory()
    if folder_path:

        while True:

            files_in_folder = os.listdir(folder_path)

            if files_in_folder:

                filtered_pdf_files = filter(
                    lambda filename: filename.lower().endswith('.pdf'), files_in_folder)

                for pdf_file in filtered_pdf_files:

                    pdf_file_full_path = f'{folder_path}/{pdf_file}'

                    if os.path.isfile(pdf_file_full_path):

                        if os.path.getsize(pdf_file_full_path) > 0:

                            with TemporaryDirectory() as tempdir:

                                images = convert_from_path(
                                    pdf_file_full_path, poppler_path=poppler_path, output_folder=tempdir, fmt='jpeg')

                                for index, image in enumerate(images):

                                    image_text = pytesseract.image_to_string(
                                        image)

                                    matched = reg_exp.search(image_text)

                                    if matched:
                                        result_string = matched.group().strip()
                                    else:
                                        result_string = 'Não encontrado'

                                    print(
                                        f'Arquivo: {pdf_file} | Página: {index+1} | Nº Guia: {result_string}')

            sleep(1)


if __name__ == '__main__':
    main()
