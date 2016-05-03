import subprocess
import os

import numpy as np
import scipy

def main():

    #gatherSentiment()

    fname = 'sentiment.txt'
    F = open(fname, 'r')
    for line in F.readlines():
        items = line.split(',')
        name = items[0]
        values = [int(item) for item in items[1:]]
        print name
        print sum(values) / float(len(values)), scipy.std(np.array(values))

def gatherSentiment():
    dataDir = 'LOTR/characterQuotes'
    speeches = [fname for fname in os.listdir(dataDir)]
    points = {'very negative' : -3, 'negative' : -1, 'neutral' : 0,
              'positive' : 1, 'very positive' : 3}
    for speech in speeches:
        speechF = os.path.join(dataDir, speech.replace(' ', '\ '))
        length = subprocess.check_output('wc -l ' + speechF, shell=True)
        if int(length.split()[0]) > 100:
            sentiment = runSentiment(speechF)
            scores = sentiment.split('\n')[1:]
            values = []
            for score in scores:
                try:
                    values.append(str(points[score.strip().lower()]))
                except KeyError:
                    continue
            print speech + ',' + ','.join(values)

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
