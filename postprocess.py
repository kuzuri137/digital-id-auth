# Post-processing after inferencing, mainly teserract ocr
import cv2
import pytesseract

# we load the tesseract ocr exe for windows
pytesseract.pytesseract.tesseract_cmd = r"D:\softwares\Tesseract-OCR\tesseract.exe"


class Postprocess:
    # this function draw the rectangles for the detected text regions
    def write(self, x, returned_img):
        c1 = tuple(x[1:3].int())
        c2 = tuple(x[3:5].int())
        cv2.rectangle(returned_img, c1, c2, (0, 255, 0), 2)
        return returned_img

    def extract_dob(self, text):  # regular expression for dob
        text = " ".join(text.split("\n")).split(" ")
        dob = ""
        for words in text:
            dob = words.split("-")
            if len(dob) == 3:
                dob = words
                break
        return dob

    def extract_id(self, text):  # regular expression for id
        text = " ".join(text.split("\n")).split(" ")
        id = ""
        for words in text:
            id = words.split(".")
            if len(id) >= 3:
                id = words
                break
        return id

    def extract_height(self, text):  # regular expression for height
        text = " ".join(text.split("\n")).split(" ")
        height = ""
        for words in text:
            height = words.split(".")
            if len(height) == 2:
                height = words
                break
        return height

    def extract_group(self, text):  # regular expression for blood group
        text = " ".join(text.split("\n")).split(" ")
        group = ""
        for words in text:
            all_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
            if words in all_groups:
                group = words
                break
        return group

    def extract_sex(self, text):  # regular expression for gender
        text = " ".join(text.split("\n")).split(" ")
        sex = ""
        for words in text:
            if words == "M" or words == "F":
                sex = words
                break
        return sex

    def extract_name(self, text):  # filtrate firstname, last name, address, id
        text = " ".join(text.split("\n")).split(" ")
        return text

    def tess_ocr(self, im, name):  # do the ocr for cropped rois detected by yolov3
        text = pytesseract.image_to_string(im)  # ocr with tesseract is done here
        extracted = ""
        if name == "dob":
            extracted = self.extract_dob(text)
        elif name == "id":
            extracted = self.extract_id(text)
        elif name == "hgs":
            h = self.extract_height(text)
            g = self.extract_group(text)
            s = self.extract_sex(text)
            extracted = [h, g, s]
        elif name == "first_name" or name == "last_name" or name == "address" or name == "id":
            text = pytesseract.image_to_string(im)
            text = "".join(text.split("APELLIDOS"))
            text = "".join(text.split("FECHA"))
            text = "".join(text.split("DE"))
            text = "".join(text.split("NACIMIENTO"))
            text = "".join(text.split("LUGAR"))
            extracted = self.extract_name(text)
            if name == "address":
                extracted = [s for s in extracted if not "NAC" in s]

        return [name, extracted]
