import requests
import time
from bs4 import BeautifulSoup


def extract_news(parser) -> list:
    """ Extract news from a given web page """
    news_list = []
    tbl_list = parser.table.find_all('table')
    tr_list = tbl_list[1].find_all('tr')


    n = 0
    for i in range(30):
            a_list_title = tr_list[n].find_all('a')
            a_list_footer = tr_list[n+1].find_all('a')
            span_list_footer = tr_list[n+1].find_all('span')

            if a_list_footer[5].string == 'discuss':
                comments = 0
            else:
                comments = a_list_footer[5].string.split()[0]
            title = a_list_title[1].string
            author = a_list_footer[0].string
            url = a_list_title[1].get('href')
            points = int(span_list_footer[0].string.split()[0])

            news_list += [(title,
                           author,
                           url,
                           comments,
                           points)]

            n += 3
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """

    return parser.find("a", {"class": "morelink"}).get('href')


def get_news(url: str, n_pages=1) -> list:
    """ Collect news from a given web page """

    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(3)
    return news

if __name__ == '__main__':
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=1)
    print(news_list)
