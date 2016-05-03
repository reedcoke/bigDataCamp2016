import os

import gensim

def main():
    malletFile = 'LOTR/mallet/lotr.mallet'
    ldaFile = 'models/lotr.lda'
    update = True

    if not os.path.exists(ldaFile) or update:
        print 'Building corpus'
        corpus = gensim.corpora.MalletCorpus(malletFile)
        print 'Training LDA'
        model = gensim.models.LdaModel(corpus, id2word=corpus.id2word,
                                       alpha='auto', num_topics=5) 
        model.save(ldaFile)
    else:
        print 'Loading trained model'

    model = gensim.models.LdaModel.load(ldaFile)
    for topic in model.show_topics(num_topics=5, num_words=5):
        print topic

if __name__ == '__main__':
    main()
