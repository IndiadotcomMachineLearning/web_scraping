import requests

from bs4 import BeautifulSoup

# from requests_html import HTMLSession

from urllib.request import Request, urlopen

import requests
import random
import re
import pandas as pd

from urllib.request import urlopen

a = {"article": [], "content_type": [], "description": [], "title": []}


def wion_summary(url):
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]

    r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
    htmlcontent = r.content
    #     soup = BeautifulSoup(htmlcontent, 'html.parser')
    #     summary = soup.find_all('body')

    # url = "https://www.wionews.com/micros/latest-cre-feed.xml?date=08112022"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    pattern_article = "<content:encoded.*?>.*?</content:encoded.*?>"
    article = re.findall(pattern_article, html, re.IGNORECASE)

    pattern_title = "<title.*?>.*?</title.*?>"
    title = re.findall(pattern_title, html, re.IGNORECASE)

    pattern_description = "<description.*?>.*?</description.*?>"
    description = re.findall(pattern_description, html, re.IGNORECASE)
    # summary = match_results.group()
    # summary = re.sub("<.*?>", "", summary) # Remove HTML tags

    #     print(category[10])
    #     print(len(category))

    for i in range(len(article)):
        char_to_replace = {'<p>': '', '</p>': '', '<p><strong>': '', '</strong></p>': '', '</a>': '', ']]></body>': '',
                           '<strong>': '', '</strong>': ''}

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

        a['article'].append(article[i][len("<content:encoded><![CDATA["):-len("</li> </ol>]]></content:encoded>'")])

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

    for k in range(len(description)):
        c = str(description[k])
        a['description'].append(
            c[c.find("<description>") + len("<description>") + len("<![CDATA["):c.find("</description>") - len("]]>")])

    for l in range(len(title)):
        c = str(title[l])
        a['title'].append(c[c.find("<title>") + len("<title>") + len("<![CDATA["):c.find("</title>") - len("]]>")])

    df = pd.DataFrame(a)
    return df

#example
#df_health = wion_summary("https://api.thehealthsite.com/index.php?c=Lateststorylist&lang=en&fromdate=2022-08-19&enddate=2022-09-19&set=1&json=")
#df_health