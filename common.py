# a common class that does most of the common tasks for all other classes
from inferencing import Inference


class Common:
    def __init__(self):
        self.all_ids = ["front", "back", "id", "last_name", "first_name", "address", "hgs", "dob"]

    def anchors(self, img):
        infer = Inference()
        return infer.infer(img)

    def crop(self, roi, img):
        left, top, right, bottom = roi
        img = img[top:bottom, left:right]
        return img

    # helps padded ocr to have most occured words
    def most_occured(self, li, name, occ):
        corrected = []
        for k in li:
            if name == "first_name" or name == "last_name":  # if ocr is a first name or last name then, we do not require number
                k = ''.join(e for e in k if e.isalnum())
            if len(k) > 0:
                corrected.append(k)
        unique = []
        count = []
        for str in corrected:
            if str in unique:
                inde = unique.index(str)
                count[inde] = count[inde] + 1
            else:
                unique.append(str)
                count.append(1)
        final = []
        for h, j in enumerate(count):
            if j >= occ:  # if occurance is greater than the threshhold then occurance is the required result
                final.append(unique[h])
        return final

    def get_padded_box(self, roi, side_pad_factor=1, vertical_pad_factor=1):  # it adds a padding to the exsiting roi
        c1 = tuple(roi[1:3].int())
        c2 = tuple(roi[3:5].int())
        left, top, right, bottom = c1[0], c1[1], c2[0], c2[1]
        left = left - (side_pad_factor * left) / 100
        top = top - (vertical_pad_factor * top) / 100
        right = right + (side_pad_factor * right) / 100
        bottom = bottom + (vertical_pad_factor * bottom) / 100
        box = left, top, right, bottom
        return box

    def mapid(self,
              elem):  # maps detected bounding box ids to its string names like dob, adddress first name and last name
        name = self.all_ids[elem[7].int()]
        return name
