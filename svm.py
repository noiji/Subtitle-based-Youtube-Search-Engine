import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

data = pd.read_csv('transcript_semicon2.csv', encoding='utf-8-sig', error_bad_lines=False, engine='python')
data2 = pd.read_csv('transcript_nonsemicon_take5_nanprob.csv', encoding='utf-8-sig', error_bad_lines=False, engine='python')
frames = [data, data2]
df1 = pd.concat(frames)
df=df1.astype(str)
df = df.replace(np.nan, 'Nan', regex=True)
del df['Unnamed: 0']
print(df)

X = df['transcript']
y = df['label']

#숫자와 엔터, 부호 없애기
df['transcript'] = df['transcript'].str.replace('\d+', '')
df = df.replace(r'\\n',' ', regex=True)
df['transcript']= df['transcript'].str.replace('[^\w\s]','')

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X = count_vect.fit_transform(X)
count_vect.vocabulary_.get(u'algorithm')
#차원이 다름
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0) #train하는 게 애초에 맞나 싶어서 이거 없애고 밑에 fit X, y로 바꿧당

# #From occurrences to frequencies
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X= tfidf_transformer.fit_transform(X)

from sklearn.linear_model import SGDClassifier
clf = SGDClassifier(loss='modified_huber', penalty='l2', alpha=0.001, random_state=42, max_iter=15, tol=0.001).fit(X, y)
predicted = clf.predict(X)
print(np.mean(predicted == y))
print(classification_report(y, predicted))
