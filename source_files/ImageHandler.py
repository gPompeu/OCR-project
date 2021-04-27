import numpy as np
import EnvironmentSettings
import pytesseract

import ImageFilters

from cv2 import cv2
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                  PDFSyntaxError)


class Image():

    def __init__(self, pilImage):
        self.bgrImage = pilToBgr(pilImage)
        self.filter()

    def filter(self):
        self.bgrImage = ImageFilters.cropWhitePadding(self.bgrImage)
        self.bgrImage = ImageFilters.cropUpperQuarter(self.bgrImage)
        self.bgrImage = ImageFilters.addBorder(self.bgrImage)
        self.bgrImage = ImageFilters.deskew(self.bgrImage)
        self.binImage = ImageFilters.threshold(self.bgrImage, 210)
        # self.binImage = ImageFilters.dilateBin(self.binImage, (1, 2))
        # ImageFilters.showImage(self.binImage, '')

    def getText(self):
        return pytesseract.image_to_string(self.binImage)


def getImagesFromPdf(filePath, outputFolder):
    return convert_from_path(filePath, poppler_path=EnvironmentSettings.popplerPath, output_folder=outputFolder)


def pilToBgr(pilImage):
    return cv2.cvtColor(np.array(pilImage), cv2.COLOR_RGB2BGR)
