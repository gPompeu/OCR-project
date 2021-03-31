import os
import PdfHandler

from time import sleep
from tkinter import filedialog
from glob import glob


class Folder:

    def askUserForFolder(self):
        self.userSelectedFolderPath = filedialog.askdirectory()

    def watchUserFolder(self):
        while True:

            pathListOfPdfFilesInFolder = getPathListOfPdfFilesInFolder(
                self.userSelectedFolderPath)

            PdfHandler.parsePdfFiles(
                pathListOfPdfFilesInFolder, self.userSelectedFolderPath)

            sleep(1)


def getPathListOfPdfFilesInFolder(folderPath):
    return list(filter(PdfHandler.checkPdfIntegrity, glob(os.path.join(folderPath, '*.pdf'))))


def getFilenameFromPath(filePath):
    return os.path.basename(filePath)


def outputListToTxtFile(list, txtFileName, separator, outputFolder):
    with open(os.path.join(outputFolder, f'{txtFileName}.txt'), 'a+') as txt:
        txt.write(f'{separator.join(list)}{separator}')


def move(filePath, baseFolder, toFolderName):
    fileName = getFilenameFromPath(filePath)
    destinationFolder = os.path.join(baseFolder, toFolderName)

    if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)

    try:
        os.replace(filePath, os.path.join(destinationFolder, fileName))
    finally:
        return
