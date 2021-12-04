# a class to initiate all the hyper parameters for yolov3
import torch

from yolo.darknet import Darknet


class Configs:
    def __init__(self):
        self.CFG = "./yolo/cfg/yolov3.cfg"
        self.WEIGHT_FILE_PATH = "./yolo/weights/yolov3_2000.weights"
        self.cuda = torch.cuda.is_available()
        self.model = Darknet(self.CFG)
        self.model.load_weights(self.WEIGHT_FILE_PATH)
        self.model.net_info["height"] = 416
        self.model.eval()
        if self.cuda:
            self.model.cuda()
        self.confidence = 0.50
        self.nms = 0.01
        self.yolo_height = 416
        self.inp_dim = self.yolo_height
        self.num_classes = 8
