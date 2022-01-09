from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs
import json

# search for news 
def search(symbol):
    ticker = symbol
    base_url = "https://duckduckgo.com/?q="
    parms = "&atb=v252-1&df=d&iar=news&ia=news"
    URL = base_url + ticker + parms
    
    # init an HTML Session
    session = HTMLSession()
    # get the html content
    response = session.get(URL)
    # execute Java-script
    response.html.render(sleep=1)
    # create bs object to parse HTML
    soup = bs(response.html.html, "html.parser")
    
    news_contents = soup.find_all('div', class_="result__body")
    newsArr = storeData(news_contents,ticker)
    return newsArr

# stores data into json file
def storeData(data,symbol):
    ticker = symbol
    contents = data
    contentsArr = []
    for content in contents:
        contentsObject = {
            "ticker": ticker.upper(),
            "title": content.find('a',class_="result__a").text, 
            "link": content.find('a',class_="result__a")["href"]
            }
        contentsArr.append(contentsObject)
    # write to json file
    with open('newsfeedData.json','w') as outfile:
        json.dump(contentsArr, outfile)
    