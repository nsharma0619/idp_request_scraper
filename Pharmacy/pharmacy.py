import mechanicalsoup
import pandas as pd
import concurrent.futures
dic = {'area of study':[],
       'course_name':[],
       'university_name':[],
       'course_fee':[],
       'course_link':[],
      }
df = pd.DataFrame(dic)

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://www.idp.com/global/search/all-pharmacy/")
count=0
while True:
    count+=1
    print(count)
    soup = browser.page
    cards = soup.find('ul', class_='product__listing product__list').find_all('li')
    for card in cards:
        dic = {}
        prd_inner_cont = card.find('div', class_='prd_inner_cont')
        right_content = card.find('div', class_='right-content')
        dic['area of study'] = 'pharmacy'
        try:
            dic['course_name'] = prd_inner_cont.find('h2').find('a').text.strip('\n')
        except:
            pass
        try:
            dic['university_name'] = prd_inner_cont.find('h3').find('a').find('span', class_='uniname').text
        except:
            pass
        try:
            score = right_content.find("div", class_="score")
            try:
                dic['course_fee'] = score.find_all("p")[1].text.replace('\xa0\n', ' ').split('?')[0].strip('\n')
            except:
                pass
            try:
                dic['course_link'] = 'https://www.idp.com' + prd_inner_cont.find('h2').find('a')['href']
            except:
                pass
        except:
            pass
        df = df.append(dic, ignore_index=True)
    next_page = soup.find('a', {'rel':'next'})
    if next_page:
        next_page_url = 'https://www.idp.com' + next_page['href']
        browser.open(next_page_url)
        continue
    break
df.to_csv("link_info.csv")