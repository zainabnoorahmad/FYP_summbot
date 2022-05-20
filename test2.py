

       #before
        #count=0
        #for i in search(query,stop=15,tld="com",lang='en'):
        #    if(count< 10):
        #        urls.append(i)
        #        #print(urls[i])
        #    count+=1
        #for url in urls:
        #    print(url)
        
        
            
            ##time.sleep(1) #to sleep 1 sec

###workingggggggggggggggggggggggggggggggggggggg



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


driver = webdriver.Chrome("E:\chromedriver.exe",options=options)
driver.set_window_position(0,-1000)


# Query to obtain links
query = 'what is NFT?'
links = [] # Initiate empty list to capture final results
# Specify number of pages on google search, each page contains 10 #links
n_pages = 2
for page in range(1, n_pages):
    url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # soup = BeautifulSoup(r.text, 'html.parser')

    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))


search = soup.find_all('div', class_="yuRUbf")


for h in search:
        links.append(h.a.get('href'))

google_domains = ( 
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

for link in links:
	print(link)