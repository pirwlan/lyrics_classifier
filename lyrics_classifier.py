import argparse
import build_classifier as bc
import util
import os
import scraper as scr
import textcleaner as tcl
import user_interaction as ui


def lyrics_classifier(parameter):

    artists = util.clean_args(parameter)

    print('[INFO] Web scraping starts...')#
    # scr.scrape_artists(artists)

    print('[INFO] Web scraping done...')
    print('[INFO] Cleaning Lyrics...')
    # tcl.clean_lyrics()
    print('[INFO] Lyrics prepared...')
    print('[INFO] Starting model training...')

    # bc.build_model()
    print('[INFO] Model trained...')
    ui.interaction()


if __name__ == '__main__':

    util.create_folder([os.path.join(os.getcwd(), 'data')])

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--artists", type=str, required=True,
                    help="enter your artist of choice")
    args = vars(ap.parse_args())

    lyrics_classifier(args)
