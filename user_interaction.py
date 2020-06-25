import os
import pandas as pd
import pickle
import textcleaner as txt


def read_model():
    """
    reads fitted model.
    Returns:
        model: sk.learn model

    """
    model_path = os.path.join(os.getcwd(), 'model', 'model.pickle')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    return model


def format_used_input(user_input):
    """
    Formats user input in format required for prediction
    Args:
        user_input:

    Returns:
        for_ui: pd.DataFrame - formatted user input
    """
    temp_list = list()
    temp_list.append(user_input)

    for_ui = pd.DataFrame(temp_list, columns=['Lyrics'])
    lyrics_list = txt.nlp_tasks(for_ui['Lyrics'])
    for_ui['lyrics_clean'] = lyrics_list

    return for_ui


def interaction():
    """
    main landing of user_interaction.py
    """

    clf = read_model()

    user_input = ''

    while user_input != 'n':

        user_input = input("Enter some lyrics: ")
        formatted_user_input = format_used_input(user_input)

        X_ui = formatted_user_input[['lyrics_clean']]
        pred = clf.predict(X_ui)

        print(f'This lyric is most likely from {pred[0]}')
        print(f'Do you want to continue?')
        user_input = input(f'Enter [y]es or [n]o: ')
