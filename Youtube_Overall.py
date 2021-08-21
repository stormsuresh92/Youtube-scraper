from requests_html import HTMLSession
import os
import pandas as pd


s = HTMLSession()

search = input('Enter keyword here: ')
print('printing data.....')

data = []

url = f'https://www.youtube.com/results?search_query={search}&sp=CAISAhAB'
response = s.get(url)
response.html.render(sleep=2, timeout=500, keep_page=True, scrolldown=100)
contents = response.html.find('#dismissible')
for item in contents:
    try:
        Channel = item.find('#text > a', first=True).text
    except:
        Channel = ''
    try:
        Title = item.find('#video-title', first=True).text
    except:
        Title = ''
    try:
        Views = item.find('#metadata-line > span:nth-child(1)', first=True).text.replace('views', '')
    except:
        Views = ''
    try:    
        Posted = item.find('#metadata-line > span:nth-child(2)', first=True).text
    except:
        Posted = ''
    try:
        url = 'https://www.youtube.com' + item.find('#video-title', first=True).attrs['href']
    except:
        url = ''
        
    dic = {
        'Channel':Channel,
        'Video_Title':Title,
        'Views':Views,
        'Posted':Posted,
        'Url':url
        }
    data.append(dic)

    
df = pd.DataFrame(data)
df.to_csv(f'{search}.csv', index=False)
print('download finished')