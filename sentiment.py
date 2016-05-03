import subprocess
import os
import codecs

import numpy as np
import scipy

def main():
    RERUN = False
    if not os.path.exists('sentiment.txt') or RERUN:
        gatherSentiment()
    showSentiment()

def showSentiment():
    fname = 'sentiment.txt'
    F = codecs.open(fname, 'r', encoding='utf8', errors='ignore')
    for line in F.readlines():
        items = line.split(',')
        name = items[0]
        values = [int(item) for item in items[1:]]
        print name
        print sum(values) / float(len(values)), scipy.std(np.array(values))

def gatherSentiment():
    #Writes to file the sentiment of all quotes by characters with at least
    #  MINQUOTES quotes
    dataDir = 'LOTR/characterQuotes'
    MINQUOTES = 100
    speeches = [fname for fname in os.listdir(dataDir)]

    #Stanford sentiment gives text ratings, we want numeric ratings
    points = {'very negative' : -3, 'negative' : -1, 'neutral' : 0,
              'positive' : 1, 'very positive' : 3}
    F = codecs.open('sentiment.txt', 'w', encoding='utf8', errors='ignore')
    for speech in speeches:
        speechF = os.path.join(dataDir, speech.replace(' ', '\ '))
        length = subprocess.check_output('wc -l ' + speechF, shell=True)
        if int(length.split()[0]) > MINQUOTES:
            sentiment = runSentiment(speechF)
            scores = sentiment.split('\n')[1:]
            values = []
            for score in scores:
                try:
                    values.append(str(points[score.strip().lower()]))
                except KeyError:
                    continue
            F.write(speech + ',' + ','.join(values) + '\n')
    F.close()

def runSentiment(fname):
    classPath = '-cp "./stanford-corenlp-full-2015-12-09/*"'
    settings = ' -mx5g edu.stanford.nlp.sentiment.SentimentPipeline'
    inputFile = ' -file ' + fname
    command = 'java ' + classPath + settings + inputFile
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = []
    while True:
        out = child.stdout.read(1)
        if out == '' and child.poll() != None:
            return ''.join(results)
        if out != '':
            results.extend(out)

if __name__ == '__main__':
    main()
