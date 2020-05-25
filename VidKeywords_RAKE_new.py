import pandas as pd
import re
import RAKE
import operator
import sys
#
df = pd.read_csv('transcript_semicon2_ko0719_perfectize_title_punen.csv', encoding='utf-8-sig')

title = df['title']
transcript = df['transcript']
link = df['link']
id = df['id']
ko = df['ko']
pun_en = df['pun_en']

only_alpha = list(transcript.copy())
for i in range(len(only_alpha)):
    only_alpha[i] = re.sub('[-:>,]', '', str(only_alpha[i]))
    only_alpha[i] = re.sub('\\d+', '', only_alpha[i])
    only_alpha[i]=only_alpha[i].strip()

rake_obj = RAKE.Rake("SmartStoplist.txt")

trans_key = []
for i in range(len(only_alpha)):
    trans_key.append(rake_obj.run(only_alpha[i]))
print(trans_key)

upper= []
uptmp = []


for i in range(len(trans_key)):
    uptmp = []
    if len(trans_key[i]) > 1:
        for j in range(6):
            uptmp.append(trans_key[i][j][0])
    upper.append(uptmp)

notime = list(transcript.copy())

for i in range(len(notime)):
    notime[i]=str(notime[i]).split(' --> ')
    del notime[i][0]
    for j in range(len(notime[i])):
        notime[i][j] = re.sub('[-:>,]', '', notime[i][j])
        notime[i][j] = re.sub('\\d+', '', notime[i][j])
        notime[i][j]=notime[i][j].strip()
print('notime')
print(notime)

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
print('onlytime')
print(onlytime)

#시간대 정보로 나눠져 있을 수 있으니 일단 onlytime에서 모든 집합을 검색해보고, 없으면 마지막 단어 빼보고, 없으면 앞 단어 빼보기
keytimestamp = []
tempppp=[]
for i in range(len(upper)):
    tempppp=[]
    for phrase in upper[i]:
        phrase = phrase.split(' ')
        while '' in phrase:
            phrase.remove('')
        tempp=[]
        temppp=[]
        for j in range(len(notime[i])):
            notime[i][j]=notime[i][j].lower()
            if len(phrase) ==1:
                if phrase[0] in notime[i][j]:
                    tempp.append(onlytime[i][j])
                else:
                    pass
            elif len(phrase) ==2:
                if phrase[0] in notime[i][j] and phrase[1] in notime[i][j]:
                    tempp.append(onlytime[i][j])
                elif phrase[0] in notime[i][j] and phrase[1] in notime[i][j+1]:
                    tempp.append(onlytime[i][j])
                else:
                    pass
            elif len(phrase) == 3 or (len(phrase) > 3 and len(notime[i]) < j+1) :
                if phrase[0] in notime[i][j]:
                    tempp.append(onlytime[i][j])
                else:
                    pass
            elif len(phrase) > 3 and len(notime[i]) > j+1 :
                if phrase[0] in notime[i][j] and phrase[1] in notime[i][j] and phrase[2] in notime[i][j] and phrase[3] in notime[i][j]:
                    tempp.append(onlytime[i][j])
                elif phrase[0] in notime[i][j] and phrase[1] in notime[i][j] and phrase[2] in notime[i][j] and phrase[3] in notime[i][j+1]:
                    tempp.append(onlytime[i][j])
                elif phrase[0] in notime[i][j] and phrase[1] in notime[i][j] and phrase[2] in notime[i][j+1] and phrase[3] in notime[i][j+1]:
                    tempp.append(onlytime[i][j])
                elif phrase[0] in notime[i][j] and phrase[1] in notime[i][j+1] and phrase[2] in notime[i][j+1] and phrase[3] in notime[i][j+1]:
                    tempp.append(onlytime[i][j])
                else:
                    pass
            else:
                pass
        if len(tempp) > 0:
            temppp = tempp[0]
        tempppp.append(temppp)
    keytimestamp.append(tempppp)

#딕셔너리 생성을 위해 빈리스트 [] 지우기
for i in range(len(upper)):
    for j in range(len(upper[i])):
        if keytimestamp[i][j] == []:
            del upper[i][j]
    while [] in keytimestamp[i]:
        keytimestamp[i].remove([])
print(keytimestamp)
print(upper)

d=[]
for i in range(len(upper)):
    x = list(sorted(dict(zip(keytimestamp[i], upper[i])).items(), reverse=False))
    d.append(x)
    print(x)
print(d)

keywordtimestmp=[]
keyword=[]
for i in range(len(d)):
    a=[]
    b=[]
    for j in range(len(d[i])):
       a.append(d[i][j][0])
       b.append((d[i][j][1]))
    keywordtimestmp.append(a)
    keyword.append(b)
print(keywordtimestmp)
print(keyword)

#pandas dataframe으로 저장
data ={'title': title, 'transcript': transcript, 'link': link, 'id':id, 'ko':ko, 'pun_en':pun_en, 'keyword timestamp':keywordtimestmp, 'keyword':keyword}
df = pd.DataFrame(data)
df.transpose

print(df)
df.to_csv(r'C:\Users\2070796\PycharmProjects\video_search\ko0719_perfectize_title_punen_keyword.csv.csv', encoding='utf-8-sig')
