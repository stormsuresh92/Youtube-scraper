from requests_html import HTMLSession
import os
import pandas as pd

s = HTMLSession()

search = input('Enter channelname here: ')
print('printing data.....')

data = []

url = f'https://www.youtube.com/c/{search}/videos'
response = s.get(url)
response.html.render(timeout=300, keep_page=True)
contents = response.html.find('#dismissible')
for item in contents:
    Title = item.find('#video-title', first=True).text
    Views = item.find('#metadata-line > span:nth-child(1)', first=True).text.replace('views', '')
    Posted = item.find('#metadata-line > span:nth-child(2)', first=True).text
    url = 'https://www.youtube.com' + item.find('#video-title', first=True).attrs['href']
    dic = {
        'Video_Title':Title,
        'Views':Views,
        'Posted':Posted,
        'Url':url
        }
    data.append(dic)

df = pd.DataFrame(data)
df.to_csv(f'{search}.csv', index=False)
print('download finished')    
    
