from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import numpy as np
import os
import pandas as pd


def lyrics_pipeline():
    """
    Pipeline for Lyrics column
    Returns:
        sklearn.Pipeline
    """
    return Pipeline([
            ('lyrics_vectorizer', CountVectorizer())
    ])


def setup_col_transformer():
    """
    Bundles all pipelines into one column transformer
    Returns:
        sklearn.ColumnTransformer
    """
    lyrics_pipe = lyrics_pipeline()

    return ColumnTransformer([
        ('lyrics_pipe', lyrics_pipe, 'Lyrics')
    ])


def clf_pipe():
    """
    Main pipeline for Grid Search
    Returns:
        sklearn.Pipeline - Main Pipeline
    """

    col_trans = setup_col_transformer()
    classifier = MultinomialNB()
    return Pipeline([('feature_engineering', col_trans),
                     ('classifier', classifier)])


def evaluate_grid(best_clf):
    """
    Shows evaluation of the best model.
    Args:
        best_clf: fitted grid-search object
    """

    print('Best parameters:')
    print(best_clf.best_params_)
    print('----------------------------------------------------------')
    print('----------------------------------------------------------')
    # get index of best modle
    best = np.argmin(best_clf.cv_results_['rank_test_score'])
    print(f'Training score: {best_clf.cv_results_["mean_train_score"][best]:.2%}')
    print('----------------------------------------------------------')

    print(f'Test score: {best_clf.cv_results_["mean_test_score"][best]:.2%}')
    print('----------------------------------------------------------')


def build_model():
    """
    Building classifier
    Returns:
        sklearn.model

    """
    df_lyrics = pd.read_csv(os.path.join(os.getcwd(),
                                         'data',
                                         'lyrics.csv'),
                            index_col=0)

    X = df_lyrics[['Lyrics']]
    y = df_lyrics['Artist']

    classifier_pipe = clf_pipe()

    grid_search_clf = GridSearchCV(estimator=classifier_pipe,
                                   param_grid=grid_parameters(),
                                   scoring='accuracy',
                                   return_train_score=True,
                                   cv=10,
                                   n_jobs=-1,
                                   verbose=1)

    best_clf = grid_search_clf.fit(X, y)

    evaluate_grid(best_clf)


def grid_parameters():
    """
    Parameter for grid search.
    Returns:
        dict - Containing parameters

    """
    return {
        'classifier__alpha': [1.0e-10, 0.1, 1, 10]}


