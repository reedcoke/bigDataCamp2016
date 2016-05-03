import os

import gensim

def main():
    malletFile = 'LOTR/mallet/lotr.mallet'
    ldaFile = 'models/lotr.lda'

    #Load the corpus created by malletize
    corpus = gensim.corpora.MalletCorpus(malletFile)
    #Train the LDA model
    model = gensim.models.LdaModel(corpus, id2word=corpus.id2word,
                                   alpha='auto', num_topics=5) 
    model.save(ldaFile)

if __name__ == '__main__':
    main()
