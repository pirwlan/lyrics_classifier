from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


import os
import pandas as pd


def lyrics_pipeline():
    return Pipeline([('lyrics_vectorizer', CountVectorizer())])


def setup_col_transformer():
    lyrics_pipe = lyrics_pipeline()

    return ColumnTransformer([
        ('lyrics_pipe', lyrics_pipe, ['Lyrics'])
    ])


def clf_pipe():

    col_trans = setup_col_transformer()
    classifier = MultinomialNB()
    return Pipeline([('feature_engineering', col_trans),
                     ('classifier', classifier)])


def build_model():
    df_lyrics = pd.read_csv(os.path.join(os.getcwd(),
                                         'data',
                                         'lyrics.csv'),
                            index_col=0)

    X = df_lyrics[['Lyrics']]
    y = df_lyrics['Artist']

    test = lyrics_pipeline()
    print(test.fit(X.value))

    # classifier_pipe = clf_pipe()
    #
    # grid_search_clf = GridSearchCV(estimator=classifier_pipe,
    #                                param_grid=grid_parameters(),
    #                                scoring='balanced_accuracy',
    #                                return_train_score=True,
    #                                cv=10,
    #                                n_jobs=-1,
    #                                verbose=1)
    #
    # best_clf = grid_search_clf.fit(X, y)
    # print(best_clf.cv_results_)

def grid_parameters():

    return {
        #'feature_engineering__lyrics_pipe__lyrics_vectorizer__'
        'classifier__alpha': [0, 0.1, 1, 10]}


