# this class extract all the elements separately
import numpy as np

from common import Common
from front_back_isolation import Isolate


class ElementExtraction:
    #extract rois detected
    def extract(self, img, side_pad_factor=1, vertical_pad_factor=1):
        boxes = Common().anchors(img)
        front, back = Isolate().mapper(img, boxes, side_pad_factor=side_pad_factor,
                                       vertical_pad_factor=vertical_pad_factor)
        return front, back

    # we remake the document again but in a customisation manner the final document will be infered again for better accuracy
    def patch(self, front, back):
        width = 1275
        height = 2100
        background = np.ones((height, width, 3), dtype="uint8") * 255
        try:
            h, w, c = front.shape
            startX, startY, endX, endY = 222, 148, 222 + w, 148 + h
            background[startY:endY, startX:endX] = front
            h, w, c = back.shape
            startX, startY, endX, endY = 222, 982, 222 + w, 982 + h
            background[startY:endY, startX:endX] = back
        except:
            background = None
        return background
