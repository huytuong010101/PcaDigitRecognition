import numpy as np
import cv2
import os


def binaryImage(pathInput, pathOutput):
    img = cv2.imread(pathInput)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    detailCnts = []
    for contour in contours:
        # approximte for circles
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        detailCnts.append((contour, len(approx), area))
    detailCnts.sort(key=lambda x: -x[2])
    x, y, w, h = cv2.boundingRect(detailCnts[1][0])
    imgCrop = thresh[y : y + h, x : x + w]
    cv2.imwrite(pathOutput, imgCrop)

