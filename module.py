import requests
from bs4 import BeautifulSoup
import time


def title_only(s):
    #sはBeautifulSoup()で作る引数
    #電撃文庫の今月と来月発売の作品タイトルとURLを抜粋。
    #タイトルと発売日を順番に表示するにはループを使う。elmsは配列だから、それで回す。
    elms = s.select(".p-books-media__title > a")
    
    for i in elms:
        print(i.contents)



    
    
