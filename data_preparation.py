from nltk.corpus import brown
import spacy

NOUN_POS_ID = 91
SPLIT = 0.65
FRAGMENT_SPLIT = 0.5


def mix_fragment_sentences(sentences, nlp):

    MAX_SENTENCE_COUNT = int(FRAGMENT_SPLIT * len(sentences))
    data = []
    labels = []

    for index, sentence in enumerate(sentences):
        curr_label = 0.0
        sequence = nlp(' '.join(sentence))
        tagged_id_sentence = [float(token.pos) for token in sequence]

        if tagged_id_sentence.count(NOUN_POS_ID) == 0:
            curr_label = 1.0

        if curr_label == 0.0 and index >= MAX_SENTENCE_COUNT:
            tagged_id_sentence.remove(NOUN_POS_ID)
            curr_label = 1.0

        data.append(tagged_id_sentence)
        labels.append(curr_label)

    return data, labels


def prep_sentence_data(n_sents=10):
    nlp = spacy.load('en')

    sentences = brown.sents()[:(n_sents+1)]

    split = int(0.65*n_sents)
    training_sentences = sentences[:split]
    testing_sentences = sentences[split:]
    X_training, Y_training = mix_fragment_sentences(training_sentences, nlp)
    X_testing, Y_testing = mix_fragment_sentences(testing_sentences, nlp)

    print X_training
    print
    print Y_training
    return X_training, Y_training, X_testing, Y_testing
