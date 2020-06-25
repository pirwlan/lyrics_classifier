from bs4 import BeautifulSoup
import os
import util
import re
import requests
import time


def get_artists_urls(artists: list):
    """
    Creates a list of artists urls
    Args:
        artists: list of artists

    Returns:
        artist_urls: list - list of artist urls

    """
    BASE_URL = 'https://www.lyrics.com/artist/'

    artists_wo_space = [artist.replace(' ', '-') for artist in artists]

    artist_urls = [f'{BASE_URL}{artist}' for artist in artists_wo_space]

    return artist_urls


def get_artist_page(artist_urls, base_path):
    """
    Accesses lyrics_htmls.com and download
    Args:
        artist_urls: list - list of artist urls
        base_path: str - Path to target folder
    """

    for artist_url in artist_urls:

        artist = artist_url.split('/')[-1]

        filename = f'{artist}.txt'
        filepath = os.path.join(base_path, filename)

        page_response = requests.get(artist_url)

        with open(filepath, 'w') as f:
            f.write(page_response.text)


def soupify(html_file):
    """

    Args:
        html_file: path to html file

    Returns:
        soupified object
    """
    with open(html_file, 'r') as f:
        html_content = f.read()
    return BeautifulSoup(html_content, 'html.parser')


def clean_title(title_raw):
    """
    Removes Brackets and strips title to prevent duplicates
    Args:
        title_raw: str - title from extracted html

    Returns:
        title_clean: str - cleaned title
    """

    regex_brackets = r'\[.*\]'
    regex_bracket = r'\[.*'
    regex_round_brackets = r'\(.*\)'
    regex_special_chars = r'[^a-zA-Z0-9 ]'

    title = re.sub(regex_brackets, '', title_raw)

    if title.find('[') != - 1:

        title = re.sub(regex_bracket, '', title)

    title = re.sub(regex_round_brackets, '', title)
    title = re.sub(regex_special_chars, '', title)

    title_clean = title.strip()

    return title_clean.lower()


def extract_lyrics(page):
    """
    reads html file and extracts all lyrics_htmls and links
    Args:
        page: soupified text file

    Returns:
        lyrics_htmls: dict - dictionary with lyric: lyric link as k, v

    """
    lyrics = dict()
    for link in page.findAll('a'):
        if str(link).find(r'/lyric/') != -1:
            if link.text not in lyrics:

                title = link.text
                title = clean_title(title)

                lyrics[title] = link.get('href')

    return lyrics


def get_lyrics(folder):
    """
    Creates a dict for every file in artist_pages containing
    Args:
        folder: Path to Artist Pages folder

    Returns:
        lyrics_htmls: dict - with Artist, Lyrics dict as k, v

    """
    lyrics = dict()
    for artist in os.listdir(folder):

        curr_file = soupify(os.path.join(folder, artist))
        lyric_links = extract_lyrics(curr_file)
        lyrics[artist[:-4]] = lyric_links

    return lyrics


def get_lyrics_htmls(lyrics):
    """
    Iterats over dictionary and downloads lyrics_htmls html in specific folders-
    Args:
        lyrics: dict - Dictionary with artist as k and lyrics - lyrics link as kv pair in v
    """

    lyrics_folder = os.path.join(os.getcwd(), 'data', 'lyrics_htmls')
    util.create_folder([lyrics_folder])

    base_url = r'https://www.lyrics.com'

    for artist in lyrics:

        artist_lyric_folder = os.path.join(lyrics_folder, artist)
        util.create_folder([artist_lyric_folder])
        for song in lyrics[artist].keys():
            lyric_url = f'{base_url}{lyrics[artist][song]}'
            file_path = os.path.join(artist_lyric_folder, f'{song.replace(" ", "_")}.txt')

            page_response = requests.get(lyric_url)

            with open(file_path, 'w') as f:
                f.write(page_response.text)

            time.sleep(1)


def convert_lyrics_html_to_txt():
    """
    Converts all lyric html files in data/lyrics_htmls into txt files containing plain text lyrics_htmls
    """
    source_path = os.path.join(os.getcwd(), 'data', 'lyrics_htmls')

    target_folder = os.path.join(os.getcwd(), 'data', 'lyrics_plain')
    util.create_folder([target_folder])

    # artist loop
    for artist in os.listdir(source_path):
        source_artist_folder = os.path.join(source_path, artist)
        target_artist_folder = os.path.join(target_folder, artist)
        util.create_folder([target_artist_folder])

        # lyric loop
        for lyric_html in os.listdir(source_artist_folder):
            if lyric_html[-4:] == '.txt':
                lyric_html_path = os.path.join(source_artist_folder, lyric_html)
                lyric_plain_path = os.path.join(target_artist_folder, lyric_html)

                lyric_soup = soupify(lyric_html_path)

                for lyric_content in lyric_soup.findAll(class_="lyric-body"):
                    lyric_plain_content = lyric_content.text

                with open(lyric_plain_path, 'w') as f:
                    f.write(lyric_plain_content)


def scrape_artists(artists: list):
    """
    main landing of scraper.

    Args:
        artists: list - list of artists
    """
    artist_folder = os.path.join(os.getcwd(), 'data', 'artist_pages')
    util.create_folder([artist_folder])

    artist_urls = get_artists_urls(artists)
    get_artist_page(artist_urls, artist_folder)

    lyrics = get_lyrics(artist_folder)
    get_lyrics_htmls(lyrics)

    convert_lyrics_html_to_txt()
