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
from QueryProcessing import *



###--url fetch

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

driver = webdriver.Chrome("chromedriver.exe",options=options)
driver.set_window_position(0,-1000)



app=Flask(__name__)
Markdown(app)


UPLOAD_FOLDER = 'tmp/'
ALLOWED_EXTENSIONS = set(['txt'])
num_words=0
num_beams=0
website_source=[]
site0=""
site1=""
site2=""
site3=""

sites=[]
urls=[]
used_urls=[]
outputs=[]
display1=display2=display3=display4=display5=""
Keywords=[]
new_display1=""
unprocessed_query=""



def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Url",methods=["GET","POST"])
def Url():
    if req.method=='POST':
        unprocessed_query=req.form['data']
        print(unprocessed_query)
        query,Keywords = query_processing( unprocessed_query)
        print(query)
        print(Keywords)

        #max_summaries = req.form['max_summaries']
        #num_beams = req.form['num_beams']
        #print(",ax-words")
        #print(max_summaries)

        #new method
        n_pages = 2
        for page in range(1, n_pages):
            url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # soup = BeautifulSoup(r.text, 'html.parser')

            search = soup.find_all('div', class_="yuRUbf")
            for h in search:
                urls.append(h.a.get('href'))


        search = soup.find_all('div', class_="yuRUbf")


        for h in search:
            urls.append(h.a.get('href'))

        google_domains = ( 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.',
                        'https://www.youtube.',
                        'https://economictimes.indiatimes.',
                        'https://www.binance.',
                        'https://www.theverge.',
                        'https://www.merriam-webster.')

        for url in urls[:]:
                if url.startswith(google_domains):
                        urls.remove(url)
        #print("------------------------------------------------------")
        #for link in urls:
        #    if(link==" "):
        #        print("empty")
        #    else:
        #        print(link)
       
    return Extract({ "urls": [
        {"url": url}
        for url in urls
    ]})

##@app.route("/Extract",methods=["GET","POST"])
def Extract(urls):
    sites=urls["urls"]

    #for site in sites:
     #   print(site)

    articles=[]
    #print(len(sites))
    working_urls=[]
    for i in range(10):

        try:
            #print(sites[i]["url"])

            if(sites[i]["url"]==" "):
                print("------------------------yes")
                continue

            #res = requests.get(sites[i]["url"])
        #html_page = res.content

            downloaded = trafilatura.fetch_url(sites[i]["url"])
            if(len(downloaded)==0):
                print("emptyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            #print("done")
            working_urls.append(sites[i]["url"])
            website_source.append(sites[i]["url"])

        #article has the content extracted using traf
           
        except TypeError:
            continue
        

        article_text = ''
        bs = BeautifulSoup(downloaded, features="lxml")
        article = bs.findAll(['p','span'])

 

        for element in article:
            page = element.getText()
            result = len(page.split())

            if result>=15:
                article_text += '\n' + ''.join(element.findAll(text = True))

        article_text = article_text.replace('\n', '') 
        
        articles.append(article_text)

        
    return Parse({ "articles": [
        {"article": article}
        for article in articles
    ]})
    


##---------------for displaying NER-----------------------

##-----------------------------------------------
 #   return urls["urls"][0]["url"]
HTML_WRAPPER = """<div style=" padding: 3px,overflow-y: scroll; width:79%">{}</div>"""
def named_entity_relationship(result1):
    NER = spacy.load("en_core_web_sm")
    NER1=[]
    
    text1= NER(result1)
    for word in text1.ents:
        NER1.append(word.text+ " " +word.label_)
        #print(word.text,word.label_)

    html = displacy.render(text1,style="ent")
    html = html.replace("\n\n","\n")
    display1 = HTML_WRAPPER.format(html)
    #print(text1)
    #spacy.displacy.render(text1, style="ent")
    # define de app
 
    return result1,display1


def Parse(articles):
     
    texts=articles["articles"]
    
    
    #used_urls.append(sites[0])
    #used_urls.append(sites[1])
    #used_urls.append(sites[2])
    #used_urls.append(sites[3])
    #used_urls.append(sites[4])

    #print("USEDD-----")
    #print(sites[0])
    #print(sites[1])
    ##print(sites[2])
    #print(sites[3])
    #print(sites[4])


    print("-------------------------------------")
    print(len(texts))
    if(texts):
        for j in range(len(texts)):
            data=texts[j]["article"]
            output=Summarize(data)
            outputs.append(output)
               

        NER1, display1=named_entity_relationship(outputs[0])
        NER2, display2=named_entity_relationship(outputs[1])
        NER3, display3=named_entity_relationship(outputs[2])
        NER4, display4=named_entity_relationship(outputs[3])
        NER5, new_display1=named_entity_relationship(outputs[4])
        NER6, new_display2=named_entity_relationship(outputs[5])
        NER7, new_display3=named_entity_relationship(outputs[6])
        NER8, new_display4=named_entity_relationship(outputs[7])



        
      
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
         
         
        #print(sites[3]['url'])
        print(unprocessed_query)
        return render_template("result.html",unprocessed_query=unprocessed_query,result1=outputs[0],result2=outputs[1],result3=outputs[2],result4=outputs[3],result5= outputs[4],display1=display1,display2=display2,display3=display3,display4=display4,new_display1=new_display1,new_display2=new_display2,new_display3=new_display3,new_display4=new_display4,url1=website_source[0],url2=website_source[1],url3=website_source[2],url4=website_source[3],url5=website_source[4])

        #return render_template("result.html",result1=outputs[0],result2=outputs[1],result3=outputs[2],result4=outputs[3],result5= outputs[4],display1=display1,display2=display2,display3=display3,display4=display4,display5=display5,site0=sites[0]['url'],site1=sites[1]['url'],site2=sites[2]['url'],site3=sites[3]['url'],keywords1=keywords1,keywords2=keywords2,keywords3=keywords3,keywords4=keywords4,keywords5=keywords5,url1=website_source[0],url2=website_source[1],url3=website_source[2],url4=website_source[3],url5=website_source[4])
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
        response = requests.post(API_URL, headers=headers, json=payload,verify=False)
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

@app.route('/fileUpload', methods = ['GET', 'POST'])
def fileUpload():
    return render_template('textFile.html')

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




def getText(url):
        downloaded = trafilatura.fetch_url(url)
        article=trafilatura.extract(downloaded)
        article_text = ''
        bs = BeautifulSoup(downloaded, features="lxml")
        article = bs.findAll('p')

        for element in article:
            page = element.getText()
            result = len(page.split())
            if result>=15:
                article_text += '\n' + ''.join(element.findAll(text = True)) 

        article_text = article_text.replace('\n', '') 
        return article_text

        #articles.append(article_text)

@app.route('/uploadUrl', methods = ['GET', 'POST'])
def uploadUrl():
    if request.method == 'POST':
        url=req.form['url']
        #print(url)
        text=getText(url)
        summary_url=Summarize(text)
        return render_template("textFile.html",text=summary_url)

@app.route('/replace1', methods = ['GET', 'POST'])
def replace1():
    print("1")
    new_text=getText(urls[4])
    new_summary1=Summarize(new_text)
    return new_summary1
    
@app.route('/replace2', methods = ['GET', 'POST'])
def replace2():
    print("2")
    new_text=getText(urls[5])
    new_summary2=Summarize(new_text)
    return new_summary2

@app.route('/replace3', methods = ['GET', 'POST'])
def replace3():
    print("3")
    new_text=getText(urls[6])
    new_summary3=Summarize(new_text)
    return new_summary3   

@app.route('/replace4', methods = ['GET', 'POST'])
def replace4():
    print("4")
    new_text=getText(urls[7])
    new_summary4=Summarize(new_text)
    return new_summary4

if __name__=='__main__':
    app.debug=True
    app.run()




