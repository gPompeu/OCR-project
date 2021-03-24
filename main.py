import os
from glob import glob
from re import compile
from tempfile import TemporaryDirectory
from time import sleep
from tkinter import Tk, filedialog

import pytesseract
from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                  PDFSyntaxError)


def main():

    remove_tkinter_root_window()

    set_tesseract_path(get_tesseract_path())

    selected_folder_path = filedialog.askdirectory()

    if selected_folder_path:

        constantly_check_folder_for_pdf_files(selected_folder_path)


def constantly_check_folder_for_pdf_files(selected_folder_path):

    while True:

        path_list_of_pdf_files_in_folder = get_pdf_files_from_folder(
            selected_folder_path)

        if path_list_of_pdf_files_in_folder:
            os.system('cls')
            print('Processando arquivos...')

            for pdf_file_path in path_list_of_pdf_files_in_folder:

                extracted_numbers_list, not_found_list = parse_pdf(
                    pdf_file_path)

                feed_csv(selected_folder_path,
                         extracted_numbers_list, not_found_list)

                move_pdf(pdf_file_path, selected_folder_path)
        else:
            os.system('cls')
            print('Aguardando arquivos...')

        sleep(1)


def move_pdf(pdf_file_path, folder_path):

    pdf_filename = get_filename_from_path(pdf_file_path)
    destination_folder = os.path.join(folder_path, 'processados')

    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    
    try:
        os.replace(pdf_file_path, os.path.join(destination_folder, pdf_filename))
    finally:
        return


def get_filename_from_path(file_path):
    return os.path.basename(file_path)


def feed_csv(output_folder, numbers, not_found):
    if numbers:
        with open(os.path.join(output_folder, 'numeros_guias.txt'), 'a+') as csv:
            csv.write(','.join(numbers)+',')

    if not_found:
        with open(os.path.join(output_folder, 'nao_encontrados.txt'), 'a+') as csv:
            csv.write('\n'.join(not_found)+'\n')


def parse_pdf(pdf_file_path):
    extracted_numbers = []
    not_found = []

    pdf_filename = get_filename_from_path(pdf_file_path)

    with TemporaryDirectory() as tempdir:
        try:
            images = pdf_to_image(pdf_file_path, tempdir)
        except:
            return extracted_numbers, not_found

        for index, image in enumerate(images):

            image_text = pytesseract.image_to_string(image)

            matched = get_regex().search(image_text)

            if matched:
                result_string = matched.group().strip()
                extracted_numbers.append(result_string)
            else:
                result_string = f'Arquivo: {pdf_filename} | Página: {index+1}'
                not_found.append(result_string)

    return extracted_numbers, not_found


def pdf_to_image(pdf_file, tempdir):
    return convert_from_path(pdf_file, poppler_path=get_poppler_path(), output_folder=tempdir)
    # , fmt='jpeg')


def get_pdf_files_from_folder(folder_path):
    path_list_of_pdf_files_in_folder = glob(os.path.join(folder_path, '*.pdf'))
    path_list_of_valid_pdf_files = list(filter(
        check_pdf_integrity, path_list_of_pdf_files_in_folder))
    return path_list_of_valid_pdf_files


def check_pdf_integrity(file_path):
    try:
        pdfinfo_from_path(file_path, poppler_path=get_poppler_path())
    except:
        return False
    else:
        return True


def set_tesseract_path(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def get_regex():
    return compile(r'\s\d{7}\s')


def get_tesseract_path():
    return './tesseract/tesseract'


def get_poppler_path():
    return './poppler/Library/bin'


def remove_tkinter_root_window():
    root = Tk()
    root.withdraw()


if __name__ == '__main__':
    main()
