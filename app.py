from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename
from geocoding import result_df_generate
import pandas as pd
import datetime
import os

app=Flask(__name__)
direct=os.getcwd()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        global filename
        file=request.files["file"]
        file.save(secure_filename(file.filename)) # input file
        result=result_df_generate(file.filename)
        os.remove(file.filename)
        try:
            filename=datetime.datetime.now().strftime("result_%Y-%m-%d-%H-%M-%S-%f"+".csv")
            result.to_csv(filename,index=None)
            return render_template("success.html",table=result.to_html(), btn="download.html")
        except:
            return render_template("success.html",table=result)
@app.route("/download/")
def download():
    print(filename)
    return send_from_directory(directory=direct,filename=filename, attachment_filename="yourfile.csv", as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)
