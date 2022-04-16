'''

from flask import Flask, render_template, url_for,request
from flask import request as req
from werkzeug.utils import secure_filename

def getFile():
    if req.method=='POST':
        ##file=req.form['textFile']
        file = request.files['file']
        file=file.save(secure_filename(f.filename))

        with open(file) as f:
            contents = f.read()
        f.close()

    return render_template("textFile.html",text=contents)
'''