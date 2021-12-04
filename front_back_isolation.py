# this isolates the front and back side of a given id card from a scanned copy
from common import Common


class Isolate:
    def mapper(self, img, boxes, side_pad_factor=1, vertical_pad_factor=1):
        original = img.copy()
        front, back = None, None
        for i in boxes:
            i = i.cpu()
            boxes = Common().get_padded_box(i, side_pad_factor=side_pad_factor,
                                            vertical_pad_factor=vertical_pad_factor)  # we add a pad factor to incread the margin
            if i[7] == 0:  # id of front side detected box is 0
                front = Common().crop(boxes, original)
            if i[7] == 1:  # id of front side detected box is 1
                back = Common().crop(boxes, original)
        return front, back
