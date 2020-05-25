import pandas as pd
from gensim.summarization.summarizer import summarize

df = pd.read_csv('newkeyword.csv.csv', encoding='utf-8-sig')

# del df['Unnamed: 0']
title = df['title']
transcript = df['transcript']
link = df['link']
id = df['id']
# only_alpha = df['only_alpha'] #이거 없애고 pun_en만 쓰는 게 더 나을 듯
ko = df['ko']
pun_en = df['pun_en']
keywordtimestmp = df['keyword timestamp']
keyword=df['keyword']

summed = []
tmp = []
for i in range(len(pun_en)):
    if pun_en[i] is not 'None':
        a=summarize(pun_en[i], word_count=50)
        print(i, a)
    else:
        a='no summary'
    tmp.append(a)
print(tmp)

# #pandas dataframe으로 저장
data ={'title': title, 'transcript': transcript, 'link': link, 'id':id, 'ko':ko, 'pun_en':pun_en, 'keyword timestamp':keywordtimestmp,
       'keyword':keyword, 'summary':tmp}
df = pd.DataFrame(data)
df.transpose

print(df)
df.to_csv(r'C:\Users\2070796\PycharmProjects\video_search\ko0722_title_punen_keyword_summary.csv', encoding='utf-8-sig')
