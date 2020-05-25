import numpy as np
import pandas as pd
data = pd.read_csv('nonsemicon.csv', encoding='utf-8-sig', error_bad_lines=False, engine='python')
data2 = pd.read_csv('semicon.csv', encoding='utf-8-sig', error_bad_lines=False, engine='python')
frames = [data, data2]
df1 = pd.concat(frames)
df=df1.astype(str)
df = df.replace(np.nan, 'Nan', regex=True)
del df['Unnamed: 0']

X = df['article']
y = df['label']

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X = count_vect.fit_transform(X)
count_vect.vocabulary_.get(u'algorithm')


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

from sklearn.naive_bayes import MultinomialNB
for alpha in [1, 1e-2, 1e-3]:
    for fit_prior in [True, False]:
        clf = MultinomialNB(alpha=alpha, fit_prior=fit_prior).fit(X_train, y_train)
        predicted = clf.predict(X_test)
        print('wo alpha=%s, fit_prior=%s일 때 accuracy ==>%s' %
              (alpha, fit_prior, np.mean(predicted == y_test)))
