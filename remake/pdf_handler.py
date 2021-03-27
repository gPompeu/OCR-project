from environment_settings import EnvironmentSettings

from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                  PDFSyntaxError)


class PdfHandler:

    def __init__(self, PdfFilePath):
        self.PdfFilePath = PdfFilePath

    def parsePdf(self):
        0==0

    def checkPdfIntegrity(self, PdfFilePath):
        try:
            pdfinfo_from_path(
                PdfFilePath, poppler_path=EnvironmentSettings.popplerPath)
        except:
            return False
        else:
            return True

class PdfText:
    def __init__(self):
        self.numbersFoundList = []
        self.notFoundDetailsList = []

        #continuaa