import requests

from bs4 import BeautifulSoup

# from requests_html import HTMLSession
import pandas as pd

# from IPython.core.display import HTML

# url = "https://www.inshorts.com/en/read/national"
a = {"Name": [], "Party": [], "Status": [], "State": [], "Constituency": [], "application uploaded date": [],
     "Father's / Husband's Name": [], "address": [], "gender": [], "age": [], "images_url": []}


# l = []


def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'


def election(URL):
    URL = URL + "?page="
    #     article = []

    #     for k in range(1,467):
    for k in range(1, 467):
        URL_final = URL + str(k)

        r = requests.get(URL_final)

        htmlcontent = r.content

        # htmlcontent

        soup = BeautifulSoup(htmlcontent, 'html.parser')

        l = []
        for elem in soup.find_all('p'):
            l.append(elem.text)
        l = l[5:]
        l_Party = l[0::4]
        l_Status = l[1::4]
        l_State = l[2::4]
        l_Constituency = l[3::4]

        d = []
        for elem in soup.find_all('h4'):
            d.append(elem.text)
        d_name = d[6:]

        images = soup.select('div img')
        images = images[1:-1]
        images_url = []
        #     for j in range(len(images)):
        #         images_url.append(images[j]['src'])

        #     images_url

        # Links
        links = soup.find_all('div', class_='img-bx')

        for i in range(len(l_Party)):
            a["Name"].append(d_name[i])
            a["Party"].append(l_Party[i][len("Party : "):])
            a["Status"].append(l_Status[i][len("Status : "):])
            a["State"].append(l_State[i][len("State : "):])
            a["Constituency"].append(l_Constituency[i][len("Constituency : "):])
            a["images_url"].append(images[i]['src'])
            #             a["image"].append(images[i]['src'])

            # get the link
            l_1 = str(links[i])
            URL_1 = l_1[l_1.find("<a href=") + len("<a href=") + 1:l_1.find("target=") - 2]
            # Go inside the link
            r_1 = requests.get(URL_1)

            htmlcontent_1 = r_1.content

            # htmlcontent

            soup_1 = BeautifulSoup(htmlcontent_1, 'html.parser')

            elements = []
            for elem in soup_1.find_all('p'):
                elements.append(elem.text)

            a["application uploaded date"].append(elements[elements.index("Application Uploaded:") + 1])

            a["Father's / Husband's Name"].append(elements[elements.index("Father's / Husband's Name: ") + 1])

            a["address"].append(elements[elements.index("Address: ") + 1])

            a["gender"].append(elements[elements.index("Gender: ") + 1])

            a["age"].append(elements[elements.index("Age: ") + 1])

    df = pd.DataFrame(a)

    #     HTML(df.to_html(escape=False,formatters=dict(image=path_to_image_html)))
    #     return HTML(df.to_html(escape=False,formatters=dict(image=path_to_image_html)))
    return df


#example
#df = election("https://affidavit.eci.gov.in/")
# df