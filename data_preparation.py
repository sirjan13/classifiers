from nltk.corpus import product_reviews_1 as dd
import spacy

NOUN_POS_ID = 91
SPLIT = 0.65
FRAGMENT_SPLIT = 0.5


def mix_fragment_sentences(sentences, max_length):

    MAX_SENTENCE_COUNT = int(FRAGMENT_SPLIT * len(sentences))
    data = []
    labels = []

    for index, sentence in enumerate(sentences):
        curr_label = 0.0

        tagged_id_sentence = sentence
        tagged_id_sentence += [0.0]*(max_length-len(tagged_id_sentence))

        if tagged_id_sentence.count(NOUN_POS_ID) == 0:
            curr_label = 1.0

        if curr_label == 0.0 and index >= MAX_SENTENCE_COUNT:
            tagged_id_sentence.remove(NOUN_POS_ID)
            tagged_id_sentence.append(0.0)
            curr_label = 1.0

        data.append(tagged_id_sentence)
        labels.append(curr_label)

    return data, labels


def prep_sentence_data(n_sents=10):
    nlp = spacy.load('en')

    sentences = dd.sents()[1500:1500+n_sents]
    print len(sentences)
    pos_tagged_sentences = []
    for sentence in sentences:
        print sentence
        if len(sentence):
            sequence = nlp(' '.join(sentence))

            pos_tagged_sentences.append([float(token.pos) for token in sequence])
        else:
            pos_tagged_sentences.append([])
    max_tokens = max([len(sentence) for sentence in pos_tagged_sentences])

    split = int(SPLIT * n_sents)
    training_sentences = pos_tagged_sentences[:split]
    testing_sentences = pos_tagged_sentences[split:]

    X_training, Y_training = mix_fragment_sentences(training_sentences, max_tokens)
    X_testing, Y_testing = mix_fragment_sentences(testing_sentences, max_tokens)

    return X_training, Y_training, X_testing, Y_testing
