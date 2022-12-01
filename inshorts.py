import requests

from bs4 import BeautifulSoup

# from requests_html import HTMLSession

import pandas as pd

# url = "https://www.inshorts.com/en/read/national"
a = {"summary": [], "headline": [], "url": [], "source_article": [], "article": []}


def inshot_summary(URL):
    #     article = []

    r = requests.get(URL)

    htmlcontent = r.content

    # htmlcontent

    soup = BeautifulSoup(htmlcontent, 'html.parser')

    #     soup.find_all("div", itemprop="articleBody")[0].text
    summary = soup.find_all("div", itemprop="articleBody")
    #     soup.find_all("span", itemprop="headline")[0].text
    headline = soup.find_all("span", itemprop="headline")

    for i in range(len(summary)):

        k = str(soup.select("div.news-card.z-depth-1")[i].select("div.news-card-footer.news-right-box", href=True))
        source_article = k[k.find("""_blank">""") + len("""_blank">"""):k.find('</a></div>')]

        #         source_article = soup.select("div.news-card.z-depth-1")[i].select("div.news-card-footer.news-right-box", href=True)[0].text

        if source_article in ['Times Now']:  # 'The Print', 'News18',
            a['summary'].append(summary[i].text)
            a['headline'].append(headline[i].text)
            b = str(soup.select("div.news-card.z-depth-1")[i].select("div.news-card-footer.news-right-box", href=True))
            url = b[b.find('https'):b.find('onclick') - 3]
            a['url'].append(url)
            a['source_article'].append(source_article)

            bsoup = BeautifulSoup(requests.get(url).content, 'html.parser')
            times_now = bsoup.find_all('div', class_="article-paragraph")
            len(times_now)
            article = []
            for j in range(len(times_now)):
                article.append(times_now[j].text)
            a['article'].append(" ".join(article))

        elif source_article in ['News18', 'The Print']:  # 'The Print', 'News18',
            a['summary'].append(summary[i].text)
            a['headline'].append(headline[i].text)
            b = str(soup.select("div.news-card.z-depth-1")[i].select("div.news-card-footer.news-right-box", href=True))
            url = b[b.find('https'):b.find('onclick') - 3]
            a['url'].append(url)
            a['source_article'].append(source_article)

            bsoup = BeautifulSoup(requests.get(url).content, 'html.parser')
            news18 = bsoup.find_all('p')
            len(news18)
            article = []
            for j in range(len(news18)):
                article.append(news18[i].text)
            a['article'].append(" ".join(article))
    df = pd.DataFrame(a)
    return df


#example
# df = inshot_summary(URL="https://www.inshorts.com/en/read")
#df
