from requests_html import HTMLSession
import pandas as pd
from alive_progress import alive_bar
from time import sleep

s = HTMLSession()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Connection':'keep-alive'
}

search = input('Enter channelname here: ')
print('Printing videos info.....')

data = []

url = f'https://www.youtube.com/c/{search}/videos'
response = s.get(url, headers=headers)
response.html.render(sleep=5, timeout=100, keep_page=True, scrolldown=5)
contents = response.html.find('#dismissible')
with alive_bar(len(contents), bar='classic2', spinner='classic') as bar:
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
        sleep(1)
        bar()

df = pd.DataFrame(data)
df.to_csv(f'{search}.csv', index=False)
print('Download completed')
input()
    
