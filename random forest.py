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

# #From occurrences to frequencies
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X= tfidf_transformer.fit_transform(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

from sklearn.ensemble import RandomForestClassifier

for n_estimators in [10, 50, 100]:
    for criterion in ['gini', 'entropy']:
        for max_depth in [None, 5, 25]:
            for min_samples_split in [2, 3, 5]:
                for min_samples_leaf in [1, 3, 5]:
                    for max_features in ['auto', 'sqrt', 'log2', None]:
                        for bootstrap in [True, False]:
                            for warm_start in [True, False]:
                                for class_weight in ['balanced','balanced_subsample', None]:
                                    clf = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split,
                                                                 min_samples_leaf=min_samples_leaf, max_features=max_features, bootstrap=bootstrap, warm_start=warm_start, class_weight=class_weight).fit(X_train, y_train)
                                    predicted = clf.predict(X_test)
                                    print('idf n_estimators=%s, criterion=%s, max_depth=%s, min_samples_split=%s, min_samples_leaf=%s, max_features=%s, bootstrap=%s, warm_start=%s, class_weight=%s일 때 accuracy ==>%s' %
                                          (n_estimators, criterion, max_depth, min_samples_split, min_samples_leaf, max_features, bootstrap, warm_start, class_weight, np.mean(predicted == y_test)))
