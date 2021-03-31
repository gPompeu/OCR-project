import numpy as np
import EnvironmentSettings
import pytesseract

from cv2 import cv2
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                  PDFSyntaxError)


class Image():

    def __init__(self, image):
        self.image = image
        self.filter()

    def filter(self):
        0 == 0

    def getText(self):
        return pytesseract.image_to_string(self.image)


def getImagesFromPdf(filePath, outputFolder):
    return convert_from_path(filePath, poppler_path=EnvironmentSettings.popplerPath, output_folder=outputFolder)


# def __init__(self, pil_image):
#     self.pil_image = pil_image
#     self.convert_from_pil_to_cv()

#     self.apply_filters()

# def convert_from_pil_to_cv(self):
#     self.image = cv2.cvtColor(np.array(self.pil_image), cv2.COLOR_RGB2BGR)

# def apply_filters(self):
#     self.remove_coloured_pixels()
#     self.deskew()

# def remove_coloured_pixels(self):
#     0==0

# def deskew(self):
#     gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

#     gray = cv2.bitwise_not(gray)

#     thresh = cv2.threshold(gray, 0, 255,
#                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#     coords = np.column_stack(np.where(thresh > 0))
#     angle = cv2.minAreaRect(coords)[-1]

#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle

#     (h, w) = self.image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(self.image, M, (w, h),
#                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

#     print("[INFO] angle: {:.3f}".format(angle))
#     # cv2.imshow("Input", self.image)
#     cv2.imshow("Rotated", rotated)
#     cv2.waitKey(0)
