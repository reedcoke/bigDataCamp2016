import os
import codecs

import nltk

def wordTokenize(fname):
    text = readFile(fname)
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    return words

def readFile(fname):
    F = codecs.open(fname, 'r', encoding='utf8', errors='ignore')
    text = F.read()
    F.close()
    return text

if __name__ == '__main__':
    base = 'LOTR/'
    raw = base + 'raw/'
    tokenized = base + 'sentences/'
    files = os.listdir(raw)
    for fname in files:
        words = wordTokenize(os.path.join(raw, fname))
        F = codecs.open(tokenized + fname, 'w', encoding='utf8', errors='ignore')
        for sentence in words:
            F.write('\t'.join(sentence) + '\n')
        F.close()
