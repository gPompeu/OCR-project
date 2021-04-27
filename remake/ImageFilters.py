from cv2 import cv2
import numpy as np


def showImage(bgrImage, text):
    cv2.imshow(text, bgrImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cropWhitePadding(bgrImage):
    gray = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8)
    coords = cv2.findNonZero(gray)
    x, y, w, h = cv2.boundingRect(coords)
    rect = bgrImage[y:y+h, x:x+w]
    return rect


def cropUpperQuarter(image):
    height = image.shape[:2][0]
    return image[:int(height/4)]


def addBorder(image):
    pix = 20
    return cv2.copyMakeBorder(image, pix, pix, pix, pix, cv2.BORDER_CONSTANT, value=[255, 255, 255])


def open(bgrImage, kernel):
    kernel = np.ones(kernel, np.uint8)
    bgrImage = cv2.morphologyEx(bgrImage, cv2.MORPH_OPEN, kernel)
    return bgrImage


def deskew(bgrImage):
    gray = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    # print("Rotadeg: {:.3f}".format(angle))
    if abs(angle) < 2:
        (h, w) = bgrImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(bgrImage, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated
    else:
        return bgrImage


def threshold(bgrImage, value):
    gray = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)
    binarized = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)[1]
    return binarized

def dilateBin(binImage, kernel):
    binInvert = cv2.bitwise_not(binImage)
    kernel = np.ones(kernel, np.uint8)
    dilated = cv2.dilate(binInvert,kernel,iterations = 1)
    return cv2.bitwise_not(dilated)
