# import modules & set up logging
import logging
import os
import codecs

import nltk
import gensim

class MySentences(object):
    #Object to stream sentences in a memory-independent way
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if fname.endswith('.txt'):
                F = codecs.open(os.path.join(self.dirname, fname), 'r',
                                encoding='utf8', errors='ignore')
                lines = F.readlines()
                F.close()
                for line in lines:
                    yield line.strip().split()

def main():
    #Stream the sentences into the model for training
    sentenceDir = 'LOTR/sentences'
    sentences = MySentences(sentenceDir) # a memory-friendly iterator
    model = gensim.models.Word2Vec(sentences)
    model.save('models/LOTRw2v')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)
    main()
