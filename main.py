from data_preparation import prep_sentence_data
from classifierNB import classify
from sklearn.metrics import accuracy_score

features_train, labels_train, features_test, labels_test = prep_sentence_data()

print features_train

clf = classify(features_train, labels_train) # doesnt work right now

pred = clf.predict(features_test)
accuracy = accuracy_score(labels_test, pred)
print accuracy
