import os
from re import compile
from tempfile import TemporaryDirectory
from time import sleep
from tkinter import Tk, filedialog

import pytesseract
from pdf2image import convert_from_path
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

        pdf_files_in_folder = get_pdf_files_from_folder(selected_folder_path)

        if pdf_files_in_folder:
            os.system('cls')
            print('Processando arquivos...')

            for pdf_file in pdf_files_in_folder:

                extracted_numbers_list, not_found_list = parse_pdf(pdf_file)

                feed_csv(selected_folder_path,
                        extracted_numbers_list, not_found_list)

                move_pdf(pdf_file, selected_folder_path)
        else:
            os.system('cls')
            print('Aguardando arquivos...')

        sleep(1)


def move_pdf(pdf_file_path, folder_path):

    pdf_filename = get_filename_from_path(pdf_file_path)
    destination_folder = f'{folder_path}/processados'

    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    os.replace(pdf_file_path, f'{destination_folder}/{pdf_filename}')

def get_filename_from_path(file_path):
    return file_path.split('/')[-1:][0]


def feed_csv(output_folder, numbers, not_found):
    if numbers:
        with open(f'{output_folder}/numeros_guias.csv', 'a+') as csv:
            csv.write(','.join(numbers)+',')

    if not_found:
        with open(f'{output_folder}/nao_encontrados.csv', 'a+') as csv:
            csv.write('\n'.join(not_found)+'\n')


def parse_pdf(pdf_file):
    extracted_numbers = []
    not_found = []

    pdf_filename = get_filename_from_path(pdf_file)

    with TemporaryDirectory() as tempdir:

        images = pdf_to_image(pdf_file, tempdir)

        for index, image in enumerate(images):

            image_text = pytesseract.image_to_string(image)

            matched = get_regex().search(image_text)

            if matched:
                result_string = matched.group().strip()
                extracted_numbers.append(result_string)
            else:
                result_string = f'{pdf_filename};{index+1}'
                not_found.append(result_string)

    return extracted_numbers, not_found


def pdf_to_image(pdf_file, tempdir):
    return convert_from_path(pdf_file, poppler_path=get_poppler_path(), output_folder=tempdir)
    # , fmt='jpeg')


def verify_its_valid_pdf(file_path):
    has_pdf_extension = file_path.lower().endswith('.pdf')
    is_a_file = os.path.isfile(file_path)
    size_greater_than_zero = os.path.getsize(file_path) > 0

    if has_pdf_extension and is_a_file and size_greater_than_zero:
        return True
    else:
        return False


def get_pdf_files_from_folder(folder_path):
    files_in_folder = os.listdir(folder_path)
    valid_pdf_files = []

    for filename in files_in_folder:
        full_path = f'{folder_path}/{filename}'

        if verify_its_valid_pdf(full_path):
            valid_pdf_files.append(full_path)

    return valid_pdf_files


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
