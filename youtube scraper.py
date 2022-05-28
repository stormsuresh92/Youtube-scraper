from requests_html import HTMLSession
import pandas as pd

s = HTMLSession()

url = 'https://www.youtube.com/results?search_query=python'

#create empty list
data = []

#create request
r = s.get(url)

#render the javascript
#if you want more results increase scrolldown value
r.html.render(sleep=3, timeout=100, keep_page=True, scrolldown=5)
cont = r.html.find('ytd-video-renderer.style-scope.ytd-item-section-renderer')

#create for loop
for item in cont:
	title = item.find('yt-formatted-string.style-scope.ytd-video-renderer', first=True).text
	videourl = 'https://www.youtube.com' + item.find('a#video-title', first=True).attrs['href']
	views = item.find('#metadata-line > span:nth-child(1)', first=True).text
	posted = item.find('#metadata-line > span:nth-child(2)', first=True).text
	Channelname = item.find('a.yt-simple-endpoint.style-scope.yt-formatted-string', first=True).text
	Channelurl = 'https://www.youtube.com' + item.find('a.yt-simple-endpoint.style-scope.yt-formatted-string', first=True).attrs['href']
	data.append([title, videourl, views, posted, Channelname, Channelurl])

df = pd.DataFrame(data, columns=['Title', 'videourl', 'views', 'posted', 'Channelname', 'Channelurl'])
df.to_csv('youtube dataset.csv', index=False)
