import os 
from flask import Flask, render_template, url_for,request
from flask import request as req
#from matplotlib import artist
import requests
from googlesearch import search
import trafilatura
from lxml import html
from bs4 import BeautifulSoup
import time
import sys
sys.path.append('D:/UNI/FYP/FYP_venv/Lib/site-packages/')
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
import textFile
from werkzeug.utils import secure_filename
import json
import spacy
from spacy import displacy
from flaskext.markdown import Markdown





app=Flask(__name__)
Markdown(app)


UPLOAD_FOLDER = 'tmp/'
ALLOWED_EXTENSIONS = set(['txt'])
num_words=0
num_beams=0

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Url",methods=["GET","POST"])
def Url():
    if req.method=='POST':
        query=req.form['data']
        num_words = req.form['max_words']
        #num_beams = req.form['num_beams']

        urls=[]
        count=0
        for i in search(query,stop=10):
            if(count<5):
                urls.append(i)
            count+=1
            ##time.sleep(1) #to sleep 1 sec

    return Extract({ "urls": [
        {"url": url}
        for url in urls
    ]})

##@app.route("/Extract",methods=["GET","POST"])
def Extract(urls):
    
    sites=urls["urls"]
    articles=[]
    for i in range(len(sites)):
        downloaded = trafilatura.fetch_url(sites[i]["url"])

        #article has the content extracted using traf
        article=trafilatura.extract(downloaded)


        article_text = ''
        bs = BeautifulSoup(downloaded, features="lxml")
        article = bs.findAll('p')

 

        for element in article:
            #print(element)
            page = element.getText()
            result = len(page.split())
            #print(result)

            if result>=15:
            #print(page)

            #print(result)
                article_text += '\n' + ''.join(element.findAll(text = True))


            # article_text += '\n' + ''.join(element.findAll(text = True))
            #print(article_text)

    
            #print("There are " + str(result) + " words.") 

        article_text = article_text.replace('\n', '') 
        
        articles.append(article_text)
        #article_paragraphs = article.findAll('p')
        #print(article_paragraphs)
        
    return Parse({ "articles": [
        {"article": article}
        for article in articles
    ]})
    


##---------------for displaying NER-----------------------

##-----------------------------------------------
 #   return urls["urls"][0]["url"]
HTML_WRAPPER = """<div style=" padding: 0.1rem,overflow: scroll">{}</div>"""
def named_entity_relationship(result1):
    NER = spacy.load("en_core_web_sm")
    NER1=[]
    
    text1= NER(result1)
    for word in text1.ents:
        NER1.append(word.text+ " " +word.label_)
        print(word.text,word.label_)

    html = displacy.render(text1,style="ent")
    html = html.replace("\n\n","\n")
    display1 = HTML_WRAPPER.format(html)
    #print(text1)
    #spacy.displacy.render(text1, style="ent")
    # define de app
 
    return result1,display1


def Parse(articles):
    texts=articles["articles"]
    outputs=[]
    if(texts):
        for j in range(len(texts)):
            data=texts[j]["article"]
            output=Summarize(data)
            outputs.append(output)
        print("~~~~~~~~~~~~~")
        print(outputs[0])
        print("~~~~~~~~~~~~~")        

        NER1, display1=named_entity_relationship(outputs[0])
        NER2, display2=named_entity_relationship(outputs[1])
        NER3, display3=named_entity_relationship(outputs[2])
        NER4, display4=named_entity_relationship(outputs[3])
        NER5, display5=named_entity_relationship(outputs[4])
        ## NER1=text1+ '' + label1
        #print("----")
        #NER1str = '\n'.join(map(str, NER1))

        #print(NER1str)
        #print("----")
        #text2,label2=named_entity_relationship(outputs[1])
        #NER2=text2+ '' + label2  
        
        #print(text2,label2)
        #text3,label3=named_entity_relationship(outputs[2])
        #NER3=text3+ '' + label3
        #text4,label4=named_entity_relationship(outputs[3])
        #NER4=text4+ '' + label4
        #text5,label5=named_entity_relationship(outputs[4])
        #NER5=text5+ '' + label5

        return render_template("result.html",result1=outputs[0],result2=outputs[1],result3=outputs[2],result4=outputs[3],result5= outputs[4],display1=display1,display2=display2,display3=display3,display4=display4,display5=display5)
#NER2=NER2,NER3=NER3,NER4=NER4,NER5=NER5


        #return summ_data(result1=outputs[0],result2=outputs[1],result3=outputs[2],result4=outputs[3],result5=outputs[4])    
    else:
        return render_template("index.html")

    


@app.route('/Summarize', methods=['POST'])
def Summarize(data):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    minL=20
    
    #num_words = request.form['max_words']
    #num_beams = request.form['num_beams']
    maxL=num_words
    print(num_words)
    
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
                "inputs":data,
    })
    #outputs.append(output[0]["summary_text"])

    return output[0]["summary_text"]



 
    





# route to get data from html form and insert data into database
##@app.route('/summ_data/result', methods=["GET", "POST"])
def summ_data(result1,result2,result3,result4,result5):
    client = MongoClient(port=27017)

# define the database to use
    db = client.summaries
    #return result
    db_entries = {}
    if request.method == "POST":
        db_entries['Query'] = request.form['data']
        db_entries['summary1'] = result1
        db_entries['summary2'] = result2
        db_entries['summary3'] = result3
        db_entries['summary4'] = result4
        db_entries['summary5'] = result5

        
        lang = []
        for i in "1234567":
            try:
                if request.form['language' + i] != "":
                    lang.append(request.form['language' + i])
            except Exception as e:
                pass
        db_entries['Language'] = lang
        db.SummaryTable.insert_one(db_entries)

    #return render_template("index.html",result=result)
    return render_template("result.html",result1=result1,result2=result2,result3=result3,result4=result4,result5= result5)



@app.route('/getFile', methods = ['GET', 'POST'])
def getFile():
    if request.method == 'POST':
        file = request.files['textFile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("tmp/", filename))

            with open('tmp/'+file.filename, encoding="utf8") as f:
                contents = f.read()
            f.close()
    summary=Summarize(contents)
    return render_template("textFile.html",text=summary)


if __name__=='__main__':
    app.debug=True
    app.run()