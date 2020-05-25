import pandas as pd
df = pd.read_csv('ko0722_title_punen_keyword_summary.csv', encoding='utf-8-sig')
del df['Unnamed: 0']
title = df['title']
transcript = df['transcript']
link = df['link']
id = df['id']
keywordtimestmp = df['keyword timestamp']
keyword = df['keyword']
summary = df['summary']
ko = df['ko']
from googletrans import Translator
translator = Translator()
import re
notime = list(transcript.copy())
import re
import time
for i in range(len(notime)):
    notime[i]=str(notime[i]).split(' --> ')
    del notime[i][0]
    for j in range(len(notime[i])):
        notime[i][j] = re.sub('[-:>,]', '', notime[i][j])
        notime[i][j] = re.sub('\\d+', '', notime[i][j])
        notime[i][j]=notime[i][j].strip()

onlytime = transcript.copy()
import string
for i in range(len(title)):
    onlytime[i]=str(transcript[i]).translate(str.maketrans('', '', string.ascii_letters))
for i in range(len(title)):
    onlytime[i] = onlytime[i].split('  ')
onlytime = list(onlytime)

for i in range(len(onlytime)):
    for j in range(len(onlytime[i])):
        onlytime[i][j] = onlytime[i][j].strip()

for i in range(len(onlytime)):
    while '' in onlytime[i]:
        onlytime[i].remove('')

for i in range(len(onlytime)):
    for j in range(len(onlytime[i])):
        onlytime[i][j] = onlytime[i][j].replace("'","").strip()

for i in range(len(onlytime)):
    while '' in onlytime[i]:
        onlytime[i].remove('')

for i in range(len(onlytime)):
    for j in range(len(onlytime[i])):
        onlytime[i][j] = onlytime[i][j][-26:-21].strip()

for i in range(len(onlytime)):
    for j in range(len(onlytime[i])):
        if ',' in onlytime[i][j]:
            onlytime[i][j]=''
        if onlytime[i][j] is '' and j > 0:
            onlytime[i][j] = onlytime[i][j-1]
        if ':' not in onlytime[i][j] and j > 0:
            onlytime[i][j] = onlytime[i][j-1]
        if len(onlytime[i][j]) is not 5 and j > 0:
            onlytime[i][j] = onlytime[i][j - 1]

for i in range(len(title)):
    if len(notime[i]) > len(onlytime[i]):
        for j in range(len(notime[i]) - len(onlytime[i])):
            onlytime[i].append(onlytime[i][0])
    elif len(onlytime[i]) > len(notime[i]):
        for j in range(len(onlytime[i]) - len(notime[i])):
            notime[i].append(notime[i][0])

    else:
        pass

input = input("검색어를 입력하세요")
input2 = translator.translate(input, dest='en').text
###tokenization&stopping
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
tokens = word_tokenize(input2)
input3 = [i for i in tokens if not i in stop_words]
print(input3)

#stemming
from nltk.stem import PorterStemmer
stemmer= PorterStemmer()
input2 = [stemmer.stem(word) for word in input3]
print(input2)
#notime[i][j]의 stemming, tokenization
for i in range(len(notime)):
    for j in range(len(notime[i])):
        notime[i][j] = word_tokenize(notime[i][j])
        for word in notime[i][j]:
            notime[i][j] = [stemmer.stem(word) for word in notime[i][j]]
print(notime[0][0])
#각 translist에 대해 검색어를 find하고 만약 있다면 timestamp와 같이 저장, 프린트한다.
result_count = 0
result_title = []
result_id = []
result_timestamp = []
unary_timestamp = []
for i in range(len(notime)):
    unary_timestamp = []
    for j in range(len(notime[i])):
        if input2 in notime[i][j]:
            if summary[i] is not 'nan':
                unary_timestamp.append(onlytime[i][j])
            else:
                pass
        else:
            pass
            # unary_timestamp.append('')
    result_timestamp.append(unary_timestamp)
#     print(unary_timestamp)
# print(result_timestamp)
result_timestamp_re=[]
for i in range(len(result_timestamp)):
    if len(result_timestamp[i]) > 0:
        result_count = result_count + 1
        result_title.append(title[i])
        result_id.append(id[i])
        result_timestamp_re.append(result_timestamp[i])
    else:
        pass


### ranking: 1) 용어 빈도 ==> 이거만 하면 훨씬 쉽다. result_timestamp 긴 순으로만 정렬하면 되니까
### 2) TOKENIZED words가 서로 가까우면 점수 +1. 애초에 이걸 찾는 notime이 가까워서 하지 않아도 될 듯

print('%s를 포함하는 영상 검색결과 총 %s개'%(input, result_count))
print('=======================================')
for i in range(result_count):
    time.sleep(0.3)
    print ('<검색결과 %s번>' %(i+1))
    print ('[%s]' %(result_title[i]))
    print('링크 바로가기:')
    for j in range(len(result_timestamp_re[i])):
        print('https://www.youtube.com/watch?v=%s&t=%s' % (result_id[i], int(result_timestamp_re[i][j][0:2]) * 60 + int(result_timestamp_re[i][j][3:])))
    print('해당 영상의 key concepts')
    print(keyword[i])
    if summary[i] == 'nan':
        pass
    else:
        print('해당 영상의 summary')
        print(summary[i])
    print("===================================================")
