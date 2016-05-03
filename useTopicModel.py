import gensim

def main():
    #Load the trained model and print some information
    ldaFile = 'models/lotr.lda'
    model = gensim.models.LdaModel.load(ldaFile)
    for topic in model.show_topics(num_topics=5, num_words=5):
        print topic

if __name__ == '__main__':
    main()
