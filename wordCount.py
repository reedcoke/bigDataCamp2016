import os
import codecs
import string

import nltk

def main():
    lotrDir = 'LOTR/raw'
    files = [fname for fname in os.listdir(lotrDir) if fname.endswith('.txt')]
    for fname in files:
        print '-' + ' '.join([n.capitalize() for n in fname.split('_')[:2]]) + '-'

        #Use the results of word_tokenize.py to get all the words in LOTR
        sentences = loadSentences(os.path.join(lotrDir, fname))
        words = [nltk.word_tokenize(sentence) for sentence in sentences]

        #Do some counting
        flatWords = sum(words, [])
        uniqueWords = set(flatWords)
        numWords = sum([len(sent) for sent in words])

        #Output the counts
        print 'Number of sentences:', len(sentences)
        print 'Number of words (tokens):', numWords
        print 'Words per sentence:', float(numWords) / len(sentences)
        print 'Number of unique words (types):', len(uniqueWords)
        print 'Types per token:', len(uniqueWords) / float(numWords)
        print

def loadSentences(fname):
    #Read in the results of word_tokenize.py
    F = codecs.open(fname, 'r', encoding='utf8', errors='ignore')
    text = [normalize(sent) for sent in nltk.sent_tokenize(F.read())]
    F.close()
    return text

def normalize(text):
    #Remove punctuation
    punctuation = ',./;\'[]\-=<>?:"{}|+_)(*&^%$#@!'
    for punc in punctuation:
        text = text.replace(punc, '')
    return text.lower()

if __name__ == '__main__':
    main()
