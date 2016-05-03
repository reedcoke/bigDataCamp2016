import os
import codecs
import operator

import nltk.tag

def extract():
    base = 'LOTR/'
    sentenceDir = base + 'sentences/'
    entityDir = base + 'entities/'
    files = [f for f in os.listdir(sentenceDir) \
            if f.endswith('.txt')]

    jarDir = 'stanford-ner-2014-06-16/stanford-ner.jar'
    jar = 'stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz'
    tagger = nltk.tag.StanfordNERTagger(jar, jarDir)

    for fname in files:
        print fname
        F = codecs.open(os.path.join(sentenceDir, fname), 'r', encoding='utf8',
                        errors='ignore')
        text = F.readlines()
        F.close()
        words = [line.strip().split('\t') for line in text]
        print 'Tagging entities'
        tags = tagger.tag_sents(words)
        print 'Extracting entities'
        entities = mergeTags(tags)
        print 'Saving', fname
        outF = codecs.open(os.path.join(entityDir, fname), 'w', encoding='utf8',
                        errors='ignore')
        for ent in entities:
            outF.write(ent + '\t' + str(entities[ent]) + '\n')
        outF.close()

def mergeTags(tags):
    entities = {}
    for sent in tags:
        inTag = False
        person = []
        for tag in sent:
            if tag[1] == 'PERSON':
                person.append(tag[0])
                inTag = True
            else:
                inTag = False
                if person != []:
                    name = ' '.join(person)
                    if name not in entities:
                        entities[name] = 0
                    entities[name] += 1
                    person = []
        if person != []:
            name = ' '.join(person)
            if name not in entities:
                entities[name] = 0
            entities[name] += 1
    return entities

def showCounts():
    base = 'LOTR/'
    entityDir = base + 'entities'
    files = [f for f in os.listdir(entityDir) if f.endswith('.txt')]
    for fname in files:
        counts = {}
        print fname
        F = codecs.open(os.path.join(entityDir, fname), 'r',
                        encoding='utf8', errors='ignore')
        entities = F.readlines()
        F.close()
        for item in entities:
            name, count = item.strip().split('\t')
            counts[name] = int(count)
        info = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(5):
            print info[i][0], info[i][1]
    return

if __name__ == '__main__':
    #extract()
    showCounts()
