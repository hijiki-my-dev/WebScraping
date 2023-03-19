import requests
from bs4 import BeautifulSoup
import time


def title_only(s):
    #sはBeautifulSoup()で作る引数
    #電撃文庫の今月と来月発売の作品タイトルとURLを抜粋。
    #タイトルと発売日を順番に表示するにはループを使って1つずつselect_oneする？
    elms = s.select(".p-books-media__title > a")
    print(elms[0])

def main():
    url = "https://dengekibunko.jp/product/newrelease-bunko.html"
    
    time.sleep(1)
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    title_only(soup)
    
    
    
    #elms = soup.find_all("a")
    #print(soup.select("h1"))
    
    #print(r.headers)
    #print(r.content)
    
    
    
if __name__ == "__main__":
    main()