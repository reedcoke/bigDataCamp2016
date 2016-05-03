import re
import os
import codecs

def main():
    patterns = buildPatterns()
    base = 'LOTR/'
    rawDir = base + 'raw/'
    entityDir = base + 'entities/'
    quoteDir = base + 'quotes/'

    #identify all quotes and speaker
    for fname in os.listdir(rawDir):
        if fname.endswith('.txt'):
            print fname
            quotes = matchPatterns(rawDir, fname, patterns)
            speakerSegments = [quote.group('speaker') for quote in quotes]
            contentSegments = [quote.group('quote') for quote in quotes]
            print len(quotes), 'quotes'
            entities = readEntities(entityDir, fname)
            print len(entities), 'entities'
            speakers = [extractSpeaker(entities, quote) for quote in speakerSegments]
            writeResults(speakers, contentSegments, os.path.join(quoteDir, fname))
    #Read in all quotes by book and rewrite them as all quotes by speaker
    mergeQuotes(base, quoteDir)

def mergeQuotes(base, quoteDir):
    #Read in a file of 'Speaker\tQuote' format and write out files for each speaker
    charDir = base + 'characterQuotes/'
    quotes = {}
    for fname in os.listdir(quoteDir):
        if fname.endswith('.txt'):
            F = codecs.open(os.path.join(quoteDir, fname), 'r',
                            encoding='utf8', errors='ignore')
            lines = [l.strip().split('\t') for l in F.readlines()]
            F.close()
            for line in lines:
                if line[0] not in quotes:
                    quotes[line[0]] = []
                quotes[line[0]].append(line[1])
    for speaker in quotes:
        F = codecs.open(os.path.join(charDir, speaker), 'w',
                        encoding='utf8', errors='ignore')
        for line in quotes[speaker]:
            F.write(line + '\n')
        F.close()

def writeResults(speakers, content, fname):
    #Write out a file of 'Speaker\tQuote' format

    #Assumes if there are multiple possible speakers
    #  the speaker is the last one
    #NOT A GOOD ASSUMPTION, JUST AN EASY ONE
    outF = codecs.open(fname, 'w', encoding='utf8', errors='ignore')
    for i in range(len(speakers)):
        if speakers[i] and content[i].strip():
            outF.write(speakers[i][-1] + '\t' + content[i] + '\n')
    outF.close()

def extractSpeaker(entities, speakerText):
    #Identify all known entities in the speaker text
    return [ent for ent in entities if ent in speakerText]

def readEntities(entityDir, fname):
    #Load all known entities
    F = codecs.open(os.path.join(entityDir, fname), 'r',
                    encoding='utf8', errors='ignore')
    ents = F.readlines()
    F.close()
    return [l.split('\t')[0] for l in ents]

def matchPatterns(rawDir, fname, patterns):
    #Match all possible (speaker, quote) instances in the text
    F = codecs.open(os.path.join(rawDir, fname), 'r',
                    encoding='utf8', errors='ignore')
    text = F.read()
    F.close()
    quotes = []
    for pat in patterns:
        quotes.extend(re.finditer(pat, text))
    return quotes

def buildPatterns():
    #Define regular expressions for finding (speaker, quote) instances
    #Quote may come before or after speaker
    #Quote may use a variety of quotation marks
    #These are far from perfect, but practically not too bad
    pat1 = re.compile("""(?P<quote>[`'"].*?[`'"])(?P<speaker>.+)""")
    pat2 = re.compile("""(?P<speaker>.+)(?P<quote>[`'"].*?[`'"])""")
    return [pat1, pat2]

if __name__ == '__main__':
    main()
