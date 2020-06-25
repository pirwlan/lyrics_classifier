from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


import numpy as np
import os
import pandas as pd
import pickle
import util


def sparse_to_dense(sparse_matrix):
    """
    Transforms sparse matrix from Vectorizer to dense matrix
    Args:
        sparse_matrix: np.array - Output array from Vector

    Returns:
        dense_matrix: np.array
    """
    return sparse_matrix.toarray()


def lyrics_pipeline():
    """
    Pipeline for Lyrics column
    Returns:
        sklearn.Pipeline
    """
    return Pipeline([
            ('lyrics_vectorizer', TfidfVectorizer()),
            ('lyrics_spacy', FunctionTransformer(sparse_to_dense)),
    ])


def setup_col_transformer():
    """
    Bundles all pipelines into one column transformer
    Returns:
        sklearn.ColumnTransformer
    """
    lyrics_pipe = lyrics_pipeline()

    return ColumnTransformer([
        ('lyrics_pipe', lyrics_pipe, 'lyrics_clean'),
    ])


def clf_pipe():
    """
    Main pipeline for Grid SearchTfidfVectorizer
    Returns:
        sklearn.Pipeline - Main Pipeline
    """

    col_trans = setup_col_transformer()
    classifier = GaussianNB()
    # classifier = MultinomialNB()
    classifier = LogisticRegression()
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
    # get index of best model
    best = np.argmin(best_clf.cv_results_['rank_test_score'])
    print(f'Training score: {best_clf.cv_results_["mean_train_score"][best]:.2%}')
    print('----------------------------------------------------------')

    print(f'Test score: {best_clf.cv_results_["mean_test_score"][best]:.2%}')
    print('----------------------------------------------------------')


def save_model(model):
    """
    Save current model
    Args:
        model: sklearn model - Fitted model
    """
    model_folder_path = os.path.join(os.getcwd(), 'model')
    util.create_folder([model_folder_path])

    model_filename = os.path.join(model_folder_path, 'model.pickle')

    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)


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

    X = df_lyrics[['lyrics_clean']]
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

    save_model(best_clf)


def grid_parameters():
    """
    Parameter for grid search.
    Returns:
        dict - Containing parameters
    """
    return {
        'classifier__C': [250, 500, 1000],
        'classifier__max_iter': [500],
        'feature_engineering__lyrics_pipe__lyrics_vectorizer__max_df': np.linspace(0.7, 1, 4),
        'feature_engineering__lyrics_pipe__lyrics_vectorizer__min_df': np.linspace(0, 0.3, 4),
        'feature_engineering__lyrics_pipe__lyrics_vectorizer__stop_words': ['english'],
        'feature_engineering__lyrics_pipe__lyrics_vectorizer__ngram_range': [(1, 1), (1, 2)]
         }



