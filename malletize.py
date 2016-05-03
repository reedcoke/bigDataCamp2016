import os
import codecs

def main():
    base = 'LOTR/'
    sentenceDir = base + 'sentences/'
    malletDir = base + 'mallet/'
    count = 0

    stopWords = loadStopwords()
    corpusF = codecs.open(os.path.join(malletDir, 'lotr.mallet'), 'w',
                          encoding='utf8', errors='ignore')
    for fname in os.listdir(sentenceDir):
        if fname.endswith('.txt'):
            F = codecs.open(os.path.join(sentenceDir, fname), 'r',
                            encoding='utf8', errors='ignore')
            lines = F.readlines()
            F.close()
            for line in lines:
                count += 1
                line = removeStops(stopWords, line)
                lineToWrite = str(count) + ' en ' + line
                lineToWrite = lineToWrite.strip() + '\n'
                corpusF.write(lineToWrite)
    corpusF.close()

def removeStops(stopwords, line):
    words = line.split('\t')
    return ' '.join([w for w in words if w.strip().lower() not in stopwords])

def loadStopwords():
    F = open('stopwords.txt', 'r')
    words = [line.lower().strip() for line in F.readlines()]
    F.close()
    return words

if __name__ == '__main__':
    main()
