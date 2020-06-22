import argparse
import helper as h
import os
import scraper as scr
import textcleaner as tcl


def lyrics_classifier(parameter):

    artists = h.clean_args(parameter)

    scr.scrape_artists(artists)

    df_lyrics = tcl.clean_lyrics()


if __name__ == '__main__':

    h.create_folder([os.path.join(os.getcwd(), 'data')])


    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--artists", type=str, required=True,
                    help="enter your artist of choice")
    args = vars(ap.parse_args())

    lyrics_classifier(args)
