import numpy as np
import cv2


def coord(image):
    rect = np.zeros((4, 2), dtype="float32")
    h, w, _ = image.shape
    rect[0] = [0, 0]
    rect[1] = [w - 1, 0]
    rect[2] = [w - 1, h - 1]
    rect[3] = [0, h - 1]
    return rect


def center(rect):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = rect
    x_mid = (x0 * x1 * (y2 - y3) + x0 * x3 * (y1 - y2) + x1 * x2 * (y3 - y0) + x2 * x3 * (y0 - y1)) /\
            ((x0 - x2) * (y1 - y3) + x1 * (y2 - y0) + x3 * (y0 - y2))
    y_mid = (x0 * y1 * y2 - x0 * y2 * y3 - x1 * y0 * y3 + x1 * y2 * y3 + x2 * y0 * (y3 - y1) + x3 * y1 * (y0 - y2)) /\
            ((x0 - x2) * (y1 - y3) + x1 * (y2 - y0) + x3 * (y0 - y2))
    crd = np.array((x_mid, y_mid), dtype = "float32")
    return crd


def distance(pt1, pt2):
    x0, y0 = pt1
    x1, y1 = pt2
    square = (y1 - y0) ** 2 + (x1 - x0) ** 2
    dist = np.sqrt(square)
    return dist


def comp(want, have):
    border = ((min(want[0][0], want[3][0]), min(want[0][1], want[1][1])),
              (max(want[1][0], want[2][0]), min(want[0][1], want[1][1])),
              (max(want[1][0], want[2][0]), max(want[2][1], want[3][1])),
              (min(want[0][0], want[3][0]), max(want[2][1], want[3][1])))

    return border


def transform(image, dest):
    dst = np.array(dest, dtype="float32")
    orig = coord(image)
    border = comp(dst, orig)

    width1 = distance(border[0], border[1])
    width2 = distance(border[2], border[3])
    maxWidth = max(int(width1), int(width2))

    height1 = distance(border[0], border[3])
    height2 = distance(border[1], border[2])
    maxHeight = max(int(height1), int(height2))
    M = cv2.getPerspectiveTransform(coord(image), dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def transpar(src):
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    return dst


def fourChannels(img):
    h, w, channels = img.shape
    if channels < 4:
        new_img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        return new_img
    return img




