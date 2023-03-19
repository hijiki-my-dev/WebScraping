import requests
from bs4 import BeautifulSoup

def main():
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    elms = soup.find_all("a")
    print(elms)
    #print(soup.select("h1"))
    
    #print(r.headers)
    #print(r.content)
    
    
    
if __name__ == "__main__":
    main()