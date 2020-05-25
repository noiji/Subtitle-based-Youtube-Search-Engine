import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from pytube import YouTube

df = pd.read_csv(r'C:\Users\2070796\PycharmProjects\video_search\transcript_semicon2_ko0719_perfectize.csv', encoding='utf-8-sig')
del df['Unnamed: 0']
transcript = df['transcript']
link = df['link']
id = df['id']
only_alpha = df['only_alpha']
ko = df['ko']

#중복삭제
df.sort_values('id', inplace=True)
df=df.drop_duplicates(subset='ko', keep='first')
print(df)

idlist = list(id)

titlelist=[]
i=1
for idd in idlist:
    print(i)
    i = i+1
    try:
        yt = YouTube('https://www.youtube.com/watch?v=%s' % idd)
        tmp = yt.title
        print(tmp)
        titlelist.append(tmp)
    except:
        titlelist.append('NaN')

#pandas dataframe으로 저장
data ={'title': titlelist, 'transcript': transcript, 'link': link, 'id':id, 'only_alpha':only_alpha, 'ko':ko}
#df = pd.DataFrame.from_dict(data, orient='index')
df = pd.DataFrame(data)
df.transpose
print(df)
df.to_csv(r'C:\Users\2070796\PycharmProjects\video_search\transcript_semicon2_ko0719_perfectize_title.csv', encoding='utf-8-sig')
