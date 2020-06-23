import argparse
import build_classifier as bc
import util
import os
import scraper as scr
import textcleaner as tcl


def lyrics_classifier(parameter):

    # artists = util.clean_args(parameter)

    # scr.scrape_artists(artists)

    # tcl.clean_lyrics()

    bc.build_model()


if __name__ == '__main__':

    util.create_folder([os.path.join(os.getcwd(), 'data')])

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--artists", type=str, required=True,
                    help="enter your artist of choice")
    args = vars(ap.parse_args())

    lyrics_classifier(args)
