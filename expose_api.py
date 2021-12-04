# this file is to expose the api end point
import os

from flask import Flask, render_template, request

import extracter

app = Flask(__name__)


@app.route('/ocr', methods=["post", "get"])
def ocr():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "bbbb"
        file = request.files['file']
        name = "./static/images/users/" + str(
            len(os.listdir("./static/images/users/"))) + ".jpg"  # temporarily store the image in a folder
        file.save(name)
        loops = extracter.extract(name)
        dicts = {"hgs": "", "first_name": "", "last_name": "", "address": "", "id": "",
                 "dob": ""}  # the fields that needs to be sent as response
        for i in range(loops):
            params = extracter.q.get()
            dicts[params[0]] = params[1]
        dicts["img"] = name
        return render_template('ocr.html', data=dicts)  # render the ocr.html with extracted fields
    return render_template('web.html')  # otherwise expose the homepage


if __name__ == '__main__':
    app.run()
