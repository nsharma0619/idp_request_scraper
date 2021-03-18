import mechanicalsoup
import pandas as pd
import concurrent.futures

df = pd.read_csv('link_info.csv')
urls = df['course_link']
dic = {
        'location':[],
        'course_link':[],
        'duration':[],
        'entry_score':[],
        'course_qualification':[],
        'intakes' : []
    }
df = pd.DataFrame(dic)

count = 0
for url in urls:
    count+=1
    dic2 = {}
    dic2['course_link'] = url
    browser = mechanicalsoup.StatefulBrowser()
    try:
        browser.open(url)
        soup = browser.page
        header = soup.find('div', class_='institution_count')
        try:
            table = soup.find('table', class_='table desktop price-table table-responsive')
            table = [i.text for i in table.find_all('td')]
            str1 = ''.join(table)
            str1 = str1.replace(',', '')
            months_master = ('january','feb','march','april','may','june','july','august','september','october','november','december')
            dic2['intakes'] = [i for i in months_master if i in str1.casefold()]
        except:
            pass

        try:
            dic2['location'] = header.find(text='Location').findNext('p').text
        except:
            dic2['location'] = None
        try:
            dic2['duration'] = header.find(text='Duration').findNext('p').text.replace('\xa0',' ')
        except:
            dic2['duration'] = None
        try:
            dic2['entry_score'] = header.find(text='Entry score').findNext('p').text    
        except:
            dic2['entry_score'] = None
        try:
            dic2['course_qualification'] = header.find(text='Qualification').findNext('p').text
        except:
            dic2['course_qualification'] = None
        print(count)
        df = df.append(dic2, ignore_index=True)
    except:
        continue
    
df.to_csv("inner_info.csv")