import EnvironmentSettings
import FolderHandler
import ImageHandler
import os

from tempfile import TemporaryDirectory
from re import compile
from pdf2image import pdfinfo_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                  PDFSyntaxError)


def checkPdfIntegrity(pdfFilePath):
    try:
        pdfinfo_from_path(
            pdfFilePath, poppler_path=EnvironmentSettings.popplerPath)
    except:
        return False
    else:
        return True


def parsePdfFiles(pathList, userFolder):
    if pathList:
        os.system('cls')
        print('Processando arquivos...')

        for pdfFilePath in pathList:
            currentPdf = Pdf(pdfFilePath)
            currentPdf.parse()
            currentPdf.output(userFolder)
            FolderHandler.move(pdfFilePath, userFolder, 'Arquivos processados')

    os.system('cls')
    print('Aguardando arquivos...')


class Pdf:

    def __init__(self, pdfFilePath):
        self.Path = pdfFilePath
        self.FileName = FolderHandler.getFilenameFromPath(self.Path)

        self.foundNumbers = []
        self.notFoundLocations = []

    def parse(self):
        with TemporaryDirectory() as tempdir:

            images = ImageHandler.getImagesFromPdf(self.Path, tempdir)

            for index, image in enumerate(images):

                pageText = ImageHandler.Image(image).getText()

                foundNumber = PageText(pageText).parse()

                if foundNumber:
                    self.foundNumbers.append(foundNumber)
                else:
                    self.notFoundLocations.append(
                        f'Arquivo: {self.FileName} | Página: {index+1}')

    def output(self, outputFolder):
        if self.foundNumbers:
            FolderHandler.outputListToTxtFile(
                self.foundNumbers, 'Números guias', ',', outputFolder)
        if self.notFoundLocations:
            FolderHandler.outputListToTxtFile(
                self.notFoundLocations, 'Não encontrados', '\n', outputFolder)


class PageText:
    def __init__(self, text):
        self.text = text
        self.regex = compile(r'\s\d{7}\s')

    def parse(self):
        matched = self.regex.search(self.text)

        if matched:
            return matched.group().strip()
        else:
            return False
