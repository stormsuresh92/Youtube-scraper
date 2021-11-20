from requests_html import HTMLSession
import pandas as pd
from alive_progress import alive_bar
from time import sleep


s = HTMLSession()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Connection':'keep-alive'
}

search = input('Enter keyword here: ')
print('Printing data.....')

data = []

url = f'https://www.youtube.com/results?search_query={search}&sp=CAISAhAB'
response = s.get(url, headers=headers)
response.html.render(sleep=5, timeout=100, keep_page=True, scrolldown=3)
contents = response.html.find('#dismissible')
with alive_bar(len(contents), bar='classic2', spinner='classic') as bar:
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
            Description = item.find('.metadata-snippet-container.style-scope.ytd-video-renderer', first=True).text
        except:
            Description = ''
        try:
            url = 'https://www.youtube.com' + item.find('#video-title', first=True).attrs['href']
        except:
            url = ''
            
        dic = {
            'Channel':Channel,
            'Video_Title':Title,
            'Views':Views,
            'Posted':Posted,
            'Description':Description,
            'Url':url
            }
        data.append(dic)
        sleep(1)
        bar()

    
df = pd.DataFrame(data)
df.to_csv(f'{search}.csv', index=False)
print('\n')
print('Download completed')
input()
