import cv2
import os
from matrixCalc import HandleMatrix
import numpy as np
import toBinaryImg


def imageToVector(path):
    img = cv2.imread(path, 0)
    img = cv2.resize(img, (15, 15), interpolation=cv2.INTER_AREA)
    vectorImg = []
    for row in img:
        vectorImg += list(row)
    return vectorImg


def showMeanImageFromMean(mean, n):
    meanImg = []
    for i in range(0, n * n, n):
        meanImg.append(mean[i : i + n])
    arrayImage = np.array(meanImg).astype(np.uint8)
    cv2.imshow("Image", arrayImage)
    cv2.waitKey()
    cv2.destroyAllWindows()


def centreToZero(a, mean):
    ans = []
    numOfColum = len(a[0])
    indexRow = 0
    for row in a:
        ansRow = []
        for item in row:
            ansRow.append(round(item - mean[indexRow], 3))
        indexRow += 1
        ans.append(ansRow)
    return np.array(ans)


def PCA(dirPath):
    """read all image"""
    listImgs = os.listdir(dirPath)
    numOfImg = len(listImgs)
    originMatrix = []
    for path in listImgs:
        originMatrix.append(imageToVector(os.path.join(dirPath, path)))
    """find the digit space"""
    digitSpace = np.array(originMatrix)
    digitSpace = digitSpace.T
    """find mean"""
    digitMean = np.mean(digitSpace, axis=1)
    # showMeanImageFromMean(digitMean, 15)
    """center to zero"""
    centerSpace = centreToZero(digitSpace, digitMean)
    """calc Cov"""
    cov = centerSpace.T.dot(centerSpace)
    v, w = np.linalg.eig(cov)
    """filter elg"""
    valueAndVector = list(zip(v, w))
    valueAndVector = sorted(valueAndVector, key=lambda x: -x[0])
    valueAndVector = valueAndVector[: int(numOfImg * 0.9)]
    filterVector = [w for _, w in valueAndVector]
    filterVector = np.array(filterVector).T
    """from eig C -> L"""
    listEigVector = centerSpace.dot(filterVector)
    pcaAns = centerSpace.T.dot(listEigVector)
    return pcaAns, digitMean, listEigVector


def distanceVector(vtA, vtB):
    tmp = 0
    for a, b in zip(vtA, vtB):
        tmp += (a - b) ** 2
    return np.sqrt(tmp)


if __name__ == "__main__":
    pca, mean, listEigVector = PCA("./trainPCA")
    # showMeanImageFromMean(mean, 15)
    # test
    path = "./sample/8/20_sample_4_.png"
    toBinaryImg.binaryImage(path, "currentTest.png")
    # pca with testImage
    test = imageToVector(os.path.join("currentTest.png"))
    test = np.array([test])
    centerImage = centreToZero(test.T, mean)
    pcaAns = centerImage.T.dot(listEigVector)
    pcaAns = pcaAns[0]
    # find the distance each pca vector
    distance = []
    for index, vt in enumerate(pca):
        distance.append((index, distanceVector(vt, pcaAns)))
    # find min distance
    distance = sorted(distance, key=lambda x: x[1])
    ans = []
    for item in distance[:5]:
        ans.append(item[0] // 10)
    digit = max(set(ans), key=ans.count)
    print(digit)
