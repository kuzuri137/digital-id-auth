# main algorithm
import queue
import threading

import cv2

from common import Common
from element_extraction import ElementExtraction
from postprocess import Postprocess
from preprocessing import Preprocess

q = queue.Queue()


def extractor(name, patch, i):  # a function which will run parallely on threads to do the ocr for each roi
    if name == "first_name" or name == "last_name" or name == "address":
        all_words = []
        iters = 6
        occurances = 3
        for factor in range(iters):  # we scan multiple times for highest ocr accuracy
            roi = Common().get_padded_box(i, side_pad_factor=5, vertical_pad_factor=factor)
            cropped = Common().crop(roi, patch)
            extracted = Postprocess().tess_ocr(cropped, name)
            for word in extracted[1]:
                all_words.append(word)
        x = Common().most_occured(all_words, name, occurances)
        final = [name, x]
    else:
        roi = Common().get_padded_box(i, side_pad_factor=5,
                                      vertical_pad_factor=5)  # if multiple scanning is not required
        cropped = Common().crop(roi, patch)
        final = Postprocess().tess_ocr(cropped, name)
    q.put(final)


def extract(path):  # thread initiator
    x = ElementExtraction()
    img = path
    img = Preprocess().to_3channels(cv2.imread(img))
    front, back = x.extract(img, side_pad_factor=10, vertical_pad_factor=1)
    patch = x.patch(front, back)
    all_elements = Common().anchors(patch)
    all_threads = []
    deco = patch.copy()
    for i in all_elements:  # 8 threads for 8 rois
        name = Common().mapid(i)
        if name == "front" or name == "back":
            continue
        t = threading.Thread(target=extractor, args=[name, patch, i])
        t.start()
        all_threads.append(t)
        deco = Postprocess().write(i, deco)
    for th in all_threads:
        th.join()
    cv2.imwrite(path, deco)  # we also write the decorated image with visible bounding boxes
    return len(all_elements) - 2 #delete 2 since we do not consider front and back for direct ocr
