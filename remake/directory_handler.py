import os

from time import sleep
from tkinter import Tk, filedialog
from glob import glob
from pdf_handler import PdfHandler


class DirectoryHandler:
    def __init__(self):
        self.removeTkinterRootWindow()
        self.askUserForFolder()

    def askUserForFolder(self):
        self.userSelectedFolderPath = filedialog.askdirectory()

    def watchUserFolder(self):
        while True:

            self.getPathListOfPdfFilesInFolder()

            self.parsePdfFiles()

            sleep(1)

    def parsePdfFiles(self):
        if self.pathListOfPdfFilesInFolder:

            for pdfFilePath in self.pathListOfPdfFilesInFolder:

                PdfHandler(pdfFilePath).parsePdf()

    def getPathListOfPdfFilesInFolder(self):
        self.pathListOfPdfFilesInFolder = glob(
            os.path.join(self.userSelectedFolderPath, '*.pdf'))

        self.pathListOfPdfFilesInFolder = list(
            filter(PdfHandler.checkPdfIntegrity, self.pathListOfPdfFilesInFolder))

    def getFilenameFromPath(self, filePath):
        #Continuar implementação

    def removeTkinterRootWindow(self):
        root = Tk()
        root.withdraw()