import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup
import json

with open('cookieFile.json') as infile:
    cookies = json.load(infile)

with open('email.txt') as infile:
    username = infile.readline().rstrip('\n')
    password = infile.readline().rstrip('\n')

head = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

already_reminded = []

if not os.path.exists('reddit.txt'):
    os.mknod('reddit.txt')
if not os.path.exists('youtube.txt'):
    os.mknod('youtube.txt')
if not os.path.exists('ins.txt'):
    with open('ins.txt','w') as outfile:
        outfile.write(1)

with open('reddit.txt') as infile:
    while(True):
        line = infile.readline()
        if not line:
            break
        already_reminded.append(line.rstrip('\n'))

def remind(title,content):
    msg = MIMEText(content, _charset="utf-8")
    msg["From"] = username
    msg["To"] = username
    msg["Subject"] = title

    s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    s.login(username, password)
    s.sendmail(username, username, msg.as_string())
    s.close()

res = requests.get('https://api.reddit.com/r/hearthstone/new/',headers=head).json()['data']['children']
for i in range(5):
    if(res[i]['data']['name'] not in already_reminded):
        if('new' in res[i]['data']['title'] or 'New' in res[i]['data']['title'] or 'NEW' in res[i]['data']['title'] or 'reveal' in res[i]['data']['title'] or 'Reveal' in res[i]['data']['title']):
            remind(res[i]['data']['title'],res[i]['data']['selftext'])
            with open('reddit.txt','a') as outfile:
                outfile.write('\n')
                outfile.write(res[i]['data']['name'])

with open('youtube.txt') as infile:
    latest = infile.readline()

video = requests.get('https://www.youtube.com/user/PlayHearthstone/videos',headers=head)
soup = BeautifulSoup(video.content, 'lxml')
for s in soup.find_all('script'):
    try:
        if(len(s.string)>100000):
            j = s.string
    except:
        pass
data = json.loads(j[j.find('{'):j.find(';')])
if(data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items'][0]['gridVideoRenderer']['videoId'] !=latest):
    remind(data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items'][0]['gridVideoRenderer']['title']['accessibility']['accessibilityData']['label'],'youtube update')
    with open('youtube.txt','w') as outfile:
        outfile.write(data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items'][0]['gridVideoRenderer']['videoId'])

with open('ins.txt') as infile:
    latest = int(infile.readline())

res = requests.get('https://www.instagram.com/graphql/query/?query_hash=cda12de4f7fd3719c0569ce03589f4c4&variables=%7B%22reel_ids%22%3A%5B%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%2217891196979359982%22%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D',headers=head,cookies=cookies).json()
if(len(res['data']['reels_media'][0]['items'])>latest):
    remind('INS','Ins update')
    with open('ins.txt','w') as outfile:
        outfile.write(str(len(res['data']['reels_media'][0]['items'])))
