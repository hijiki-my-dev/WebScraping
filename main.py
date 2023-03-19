import requests as re
from bs4 import BeautifulSoup as bs

def main():
    url = "https://www.hijiki-blog.org/2022/01/01/light-novel-recommend/"
    r = re.get(url)
    
    soup = bs(r.content, "html.parser")
    
    print(soup.select("h1"))
    
    #print(r.headers)
    #print(r.content)
    
    
    
    
    
if __name__ == "__main__":
    main()