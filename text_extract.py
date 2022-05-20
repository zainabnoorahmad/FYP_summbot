#NO 1 yet
# workinggggg

"""
import trafilatura
downloaded = trafilatura.fetch_url('https://adrien.barbaresi.eu/blog/trafilatura-main-text-content-python.html')
print(trafilatura.extract(downloaded))
"""


# trying adding beautiful soup with trafilautrura

# work on separating headings and text


import trafilatura
from lxml import html
from bs4 import BeautifulSoup


import requests

#url = 'https://www.creativebloq.com/features/what-are-nfts'
#res = requests.get(url)
#html_page = res.content

downloaded = trafilatura.fetch_url('https://www.merriam-webster.com/dictionary/summarization')

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
print(article_text)
 
#article_paragraphs = article.findAll('p')
#print(article_paragraphs)