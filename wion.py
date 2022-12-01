import requests

from bs4 import BeautifulSoup

# from requests_html import HTMLSession

from urllib.request import Request, urlopen

import requests
import random
import re
import pandas as pd

from urllib.request import urlopen
import datetime

a = {"article": [], "content_type": [], "category": [], 'date': []}


def wion_scrubbing(start_date, end_date):
    url = ''

    # start = datetime.datetime.strptime("21-06-2022", "%d-%m-%Y")
    # end = datetime.datetime.strptime("23-06-2022", "%d-%m-%Y")
    start = datetime.datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.datetime.strptime(end_date, "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    datelist = []
    for date in date_generated:
        datelist.append(date.strftime("%d-%m-%Y"))
    datelist = [re.sub('-', '', i) for i in datelist]
    # datelist

    for l in datelist:
        url = "https://www.wionews.com/micros/latest-cre-feed.xml?date=" + str(l)

        #     def wion_summary(URL):

        user_agents_list = [
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]

        r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
        htmlcontent = r.content
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        article = soup.find_all('body')

        # url = "https://www.wionews.com/micros/latest-cre-feed.xml?date=08112022"
        page = urlopen(url)
        html = page.read().decode("utf-8")

        pattern_category = "<category.*?>.*?</category.*?>"
        category = re.findall(pattern_category, html, re.IGNORECASE)
        # summary = match_results.group()
        # summary = re.sub("<.*?>", "", summary) # Remove HTML tags

        #     print(category[10])
        #     print(len(category))

        for i in range(len(article)):
            char_to_replace = {'<p>': '', '</p>': '', '<p><strong>': '', '</strong></p>': '', '</a>': '',
                               ']]></body>': '', '<strong>': '', '</strong>': ''}

            # Iterate over all key-value pairs in dictionary
            for key, value in char_to_replace.items():
                # Replace key character with value character in string
                article[i] = re.sub(key, value, str(article[i]))
                pattern = "<div.*?>.*?</div.*?>"
                content_type = re.findall(pattern, article[i], re.IGNORECASE)
                if len(content_type) != 0:
                    article[i] = article[i].replace(content_type[0], '')
                else:
                    pass

            a['article'].append(article[i][15:])

        pattern_content_type = "<content_type.*?>.*?</content_type.*?>"
        content_type = re.findall(pattern_content_type, html, re.IGNORECASE)
        # content_type = content_type.group()
        #     content_type = re.sub("<.*?>", "", content_type) # Remove HTML tags

        #     print(content_type[0])
        #     print(len(content_type))
        for j in range(len(content_type)):
            b = content_type[j]

            a['content_type'].append(b[b.find("<content_type>") + len("<content_type>"):b.find("</content_type>")])
        #         a['content_type'].append(content_type[j])

        for k in range(len(category)):
            c = str(category[k])
            a['category'].append(c[c.find("<category>") + len("<category>"):c.find("</category>")])
            a['date'].append(l)
    df = pd.DataFrame(a)
    return df

#example
# df = wion_scrubbing("21-06-2022", "18-11-2022")
#df