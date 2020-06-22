import os
import re


def clean_args(args):
    """
    Extracts artists from input arguments.
    Args:
        args: argparser object - containing the artist key

    Returns:
        artists: list - list of artists

    """
    artists_raw = args['artists']

    if artists_raw.find('"') == -1:
        return artists_raw.split(' ')

    artists = list()
    regex = r'".*?"'

    indeces = re.finditer(regex, artists_raw)

    for index in indeces:
        artists.append(artists_raw[index.span()[0] + 1: index.span()[1] - 1])

    return artists


def create_folder(path_list):
    """
    Safely creates all folders in list

    Args:
        path_list: list - list of pasts

    """

    for path in path_list:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass