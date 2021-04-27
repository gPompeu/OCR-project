import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
from matplotlib.colors import hsv_to_rgb
import numpy as np
from cv2 import cv2


def vizHsvSpace(bgrImage):
    rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)

    pixel_colors = rgbImage.reshape(
        (np.shape(rgbImage)[0]*np.shape(rgbImage)[1], 3))
    norm = colors.Normalize(vmin=-1., vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()

    hsvImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsvImage)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")

    axis.scatter(h.flatten(), s.flatten(), v.flatten(),
                 facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show()


def vizRgbSpace(bgrImage):
    rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)

    r, g, b = cv2.split(rgbImage)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")

    pixel_colors = rgbImage.reshape(
        (np.shape(rgbImage)[0]*np.shape(rgbImage)[1], 3))
    norm = colors.Normalize(vmin=-1., vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()

    axis.scatter(r.flatten(), g.flatten(), b.flatten(),
                 facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    plt.show()


def vizHsvColor(hsv):
    square = np.full((10, 10, 3), hsv, dtype=np.uint8) / 255.0
    plt.subplot(1, 2, 1)
    plt.imshow(hsv_to_rgb(square))
    plt.show()
