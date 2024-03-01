import numpy as np
import cv2
from imgprocessing import processed

vid = cv2.VideoCapture(0)

while (True):
    ret, img = vid.read()
    maskx = 500
    masky = 180
    maskw = 920
    maskh = 720
    maskimg = processed(img=img, maskx=maskx, masky=masky, maskw=maskw, maskh=maskh)

    contours, hierarchy = cv2.findContours(maskimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours is not None and len(contours) >= 2:
        midline = []
        contours = sorted(contours, key=cv2.contourArea, reverse=False)
        contour1 = contours[0]
        contour2 = contours[-1]
        a1 = np.array(contour1)[:, 0, :]
        a2 = np.array(contour2)[:, 0, :]
        cv2.polylines(img, [np.array(a1)], False, (255, 0, 0), 3)
        cv2.polylines(img, [np.array(a2)], False, (0, 0, 255), 3)


        # NEWLY IMPLEMENTED CODE
        min_a1_x, max_a1_x = min(a1[:, 0]), max(a1[:, 0])
        new_a1_x = np.linspace(min_a1_x, max_a1_x, 100)
        a1_coefs = np.polyfit(a1[:, 0], a1[:, 1], 4) # turns array 1 into a polynomial
        new_a1_y = np.polyval(a1_coefs, new_a1_x) # evaluates polynomial at specific value

        min_a2_x, max_a2_x = min(a2[:, 0]), max(a2[:, 0])
        new_a2_x = np.linspace(min_a2_x, max_a2_x, 100)
        a2_coefs = np.polyfit(a2[:, 0], a2[:, 1], 3)
        new_a2_y = np.polyval(a2_coefs, new_a2_x)

        # min_a1_x, max_a1_x = min(a1[:,0]), max(a1[:,0])
        # min_a2_x, max_a2_x = min(a2[:,0]), max(a2[:,0])
        #
        # new_a1_x = np.linspace(min_a1_x, max_a1_x, 100)
        # new_a2_x = np.linspace(min_a2_x, max_a2_x, 100)
        #
        # new_a1_y = np.interp(new_a1_x, a1[:,0], a1[:,1])
        # new_a2_y = np.interp(new_a2_x, a2[:,0], a2[:,1])


        midx = [np.mean([new_a1_x[i], new_a2_x[i]]) for i in range(100)]
        midy = [np.mean([new_a1_y[i], new_a2_y[i]]) for i in range(100)]

        print(midx)
        print(midy)

        for i in range(min(len(midx),  len(midy))):
            midline.append((midx[i], midy[i]))

        midline_array = np.array(midline, dtype=np.int32)
        cv2.polylines(img, [midline_array], False, (0, 255, 0), 3)

        cv2.rectangle(img, (maskx, masky), (maskx + maskw, masky + maskh), (255, 255, 255), 3)
        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
