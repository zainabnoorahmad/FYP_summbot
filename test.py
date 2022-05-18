
#fetch urls
# change query with the query from user

from googlesearch import search
query = "what is nft?"
urls=[]
count=0

for i in search(query,tld="com", num=10, stop=10,lang='en'): 
            if(count<10):
                urls.append(i)
            
            count+=1
 
for url in urls:
    print(url)





  
 
 

