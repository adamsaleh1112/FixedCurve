import cv2
import numpy as np

def processed(img, maskx, masky, maskw, maskh):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)
    # MASK VARIABLES
    x = maskx # mask x, y, w, h
    y = masky
    w = maskw
    h = maskh
    mask = np.zeros(edges.shape[:2], np.uint8)
    mask[y:y + h, x:x + w] = 255
    maskimg = cv2.bitwise_and(edges, edges, mask=mask)

    return maskimg