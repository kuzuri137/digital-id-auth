# OCR for eKYC and digital authentication
Introduction
--------------------
This is an application to perform OCR for ID card images with an accuracy vs fail safe algorithm

Software and Hardware Specs
------------------------
Required software: Python3.6 or higher
Required hardwares: CPU 4core 16gb | GPU at least 4gb ddr4 NVIDIA gtx Card
OS: windows 10 or ubuntu 16.0 or higher

_To install the dependent packages: Run_ `pip install -r requirements.txt`  

Before you run: Download and save the weight files in **yolo/weights** folder
Download the weights from here: https://drive.google.com/file/d/1zozKjHZWqwu5WyVjfmFHRGjgz98qi1C3/view?usp=sharing

To run this application
-------------------------------
1. Start the flask server --> `python expose_api.py`
2. Visit the url for dummy testing https://ip_addres:5555/ocr
3. Upload an image and check the ocr output

_Current accuracy of the application is above 78% approximately_
