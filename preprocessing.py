# This file is mainly to do the pre-processing of the image before inferencing
import cv2
import imutils
import torch


class Preprocess:

    def prep_image(self, img, inp_dim):
        img = self.to_3channels(img)
        orig_im = img.copy()
        # resize the image to make it infer with yolov3
        img = cv2.resize(orig_im, (inp_dim, inp_dim), interpolation=cv2.INTER_CUBIC)
        img_ = img[:, :, ::-1].transpose((2, 0, 1)).copy()
        img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
        return img_

    def to_3channels(self, img):
        gray = img
        if len(img.shape) >= 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #convert a colored image to black and white but having 3 channels
        img[:, :, 0] = gray
        img[:, :, 1] = gray
        img[:, :, 2] = gray
        img = imutils.resize(img, width=1275)
        return img
