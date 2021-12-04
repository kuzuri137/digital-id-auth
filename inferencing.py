# mainly does the inferencing of all types
from hyperparameters import Configs
from preprocessing import Preprocess
from yolo.util import *


class Inference:
    def __init__(self):
        self.configs = Configs()  # load all the hyperparameters and configs

    def infer(self, img):
        if img is None:
            raise ValueError("Either front or back side of an image is not detected properly")
        preprocess = Preprocess()
        original = img.copy()
        img = preprocess.prep_image(img, self.configs.inp_dim)
        if self.configs.cuda:
            img = img.cuda()
        model = self.configs.model
        # actual pytorch inferencing happens here
        output = model(Variable(img), self.configs.cuda)
        output = write_results(output, self.configs.confidence, self.configs.num_classes, nms=True,
                               nms_conf=self.configs.nms)
        output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(self.configs.inp_dim)) / self.configs.inp_dim
        output[:, [1, 3]] *= original.shape[1]
        output[:, [2, 4]] *= original.shape[0]
        return output
