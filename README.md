# Lyrics Classifier

This is a simple program to predict, which artist sang the lyrics we enter in the command line. It applies NLP techniques on lyrics, downloaded from  [Lyrics.com](www.lyrics.com). 



##### How to get started - Quick Tour

Please choose two artists you are interested in comparing and enter them using the -a argument. For example, if you want to compare the lyrics from Moby and Kate Tempest please enter:

```
python lyrics_classifier.py -a '"Moby" "Kate Tempest"'
```

Please note, that you should encompass all artists in double quotes, to facilitate name extraction.

After a couple of minutes, you are asked to enter some Lyrics, and the program will then predict which of the artists has most likely performed the song. If you want to stop entering, just enter "quit" as a input.



##### The deep dive

The entered artists will be used to scrape the web page [Lyrics.com](www.lyrics.com) using `BeautifulSoup`, a python module for scraping the world wide web. 

After all songs of each artist have been downloaded will be saved as plain text. Then, these files are read in, and each lyric is tokenized and reduced to its stem using `spacy`, a popular NLP libary. 

To these lyrics, a Bag of Words model is applied, which counts the occurrence of each word per lyrics, and determines a distribution of word patterns per lyrics. This is down using the `TfidfVectorizer`, which combines the counting of the words, and the normalization of the counts. 

The normalized word counts are used to train a `sklearn` Logistic Regression classification model learning which artists uses which word distribution patterns. 



#### Requirements

You can find all necessary dependencies in the requirements.txt files. 