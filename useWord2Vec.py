import gensim

def main():
    model = gensim.models.Word2Vec.load('models/LOTRw2v')
    print model.doesnt_match(['Bilbo', 'Frodo', 'Sam', 'Pippin', 'Merry'])
    print model.similarity('ghost', 'spirit')
    print model.most_similar(positive=['bread'])
    print model.most_similar(positive=['lembas'])

if __name__ == '__main__':
    main()
