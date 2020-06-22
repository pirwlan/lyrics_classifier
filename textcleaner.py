import os
import pandas as pd
import re


def read_lyrics(lyrics_filepath):
    """
    reads lyrics from txtfile
    Args:
        lyrics_filepath: path to lyricsfile

    Returns:
        lyrics: str - lyrics as string
    """
    with open(lyrics_filepath, 'r') as lyrics_file:
        lyrics = lyrics_file.read()

    regex_special_chars = r'[\n]|[\r]|\[.*\]|[\t]|Bridge:'

    lyrics = re.sub(regex_special_chars, ' ', lyrics)

    regex_mul_spaces = r'[\s]{2,}'

    lyrics = re.sub(regex_mul_spaces, ' ', lyrics)

    return lyrics


def clean_lyrics():
    """
    Landing of textcleaner.py

    Returns:
        df_data: pd.DataFrame - Dataframe containing Lyrics and artist as words
    """
    lyrics_path = os.path.join(os.getcwd(),
                               'data',
                               'lyrics_plain')
    lyrics_list = list()

    for artist in os.listdir(lyrics_path):
        artist_lyrics_path = os.path.join(lyrics_path,
                                          artist)

        for lyrics_file in os.listdir(artist_lyrics_path):
            lyrics_filepath = os.path.join(artist_lyrics_path,
                                           lyrics_file)

            lyrics = read_lyrics(lyrics_filepath)
            lyrics_list.append([lyrics, artist])

    df_data = pd.DataFrame(lyrics_list, columns=['Lyrics', 'Artist'])
    df_data.to_csv(os.path.join(os.getcwd(),
                                'data',
                                'lyrics.csv'))

    return df_data
