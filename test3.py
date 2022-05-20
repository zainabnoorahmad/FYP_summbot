import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import urllib.request
from bs4 import BeautifulSoup as bs



links=[]

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)

        return response

    except requests.exceptions.RequestException as e:
        print(e)

 

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)


    links = list(response.html.absolute_links)
      

    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube.',
                      'https://economictimes.indiatimes.',
                      'https://www.binance.',
                      'https://www.theverge.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)






    return links


links=scrape_google("what is nft?")


 

for link in links:
    print(link)

    #r = requests.get(link)
    #soup = bs(r.content, 'lxml')
    #title_of_web_page=soup.select_one('title').text
     
    #print(title_of_web_page)

   # if title_of_web_page:
    #    print(title_of_web_page)
    


    

