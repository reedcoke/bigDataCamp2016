import os
import codecs

def main():
    #Create gensim-friendly text files in the mallet format
    #Required for topic modeling with gensim
    base = 'LOTR/'
    sentenceDir = base + 'sentences/'
    malletDir = base + 'mallet/'
    count = 0

    #Load in the stopword file in this repo
    #  Includes punctuation
    stopWords = loadStopwords()
    corpusF = codecs.open(os.path.join(malletDir, 'lotr.mallet'), 'w',
                          encoding='utf8', errors='ignore')
    for fname in os.listdir(sentenceDir):
        if fname.endswith('.txt'):
            F = codecs.open(os.path.join(sentenceDir, fname), 'r',
                            encoding='utf8', errors='ignore')
            lines = F.readlines()
            F.close()

            #Write the new lines to mallet/lotr.mallet in the mallet format
            #line_number language word1 word2 word3 etc
            for line in lines:
                count += 1
                line = removeStops(stopWords, line)
                lineToWrite = str(count) + ' en ' + line
                lineToWrite = lineToWrite.strip() + '\n'
                corpusF.write(lineToWrite)
    corpusF.close()

def removeStops(stopwords, line):
    #Keep only words not present in the stopword list
    words = line.split('\t')
    return ' '.join([w for w in words if w.strip().lower() not in stopwords])

def loadStopwords():
    #Read the stopword list
    F = open('stopwords.txt', 'r')
    words = [line.lower().strip() for line in F.readlines()]
    F.close()
    return words

if __name__ == '__main__':
    main()
