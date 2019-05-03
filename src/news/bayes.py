import math
import collections


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.chance = {}
        self.p_labels = []
        self.amount = 0
        self.labels = []

    def fit(self, X: list, y: list) -> None:
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [i for i in set(y)]
        self.labels.sort()
        self.amount = len(self.labels)

        docs = [[] for l in range(len(X))]
        for i in range(len(X)):
            docs[i] = [X[i], y[i]]

        table = {}

        for i in range(len(X)):
            words = X[i].split()
            for word in words:
                table[word] = [0]*self.amount

        for k in range(self.amount):
            for i in range(len(X)):
                words = X[i].split()
                for word in words:
                    if docs[i][1] == self.labels[k]:
                        table[word][k] += 1

        for i in range(self.amount):
            counter = collections.Counter()
            for j in docs:
                counter[j[1]] += 1

        D = len(docs)
        self.p_labels = [math.log(counter[label] / D) for label in self.labels]

        V = len(table)

        L = {}
        for label in self.labels:
            L[label] = 0
            for word in table:
                L[label] += table[word][self.labels.index(label)]

        for num in range(len(X)):
            string = X[num]
            string = string.split()
            for word in string:
                self.chance[word] = [label for label in self.labels]
                for label in self.labels:
                    self.chance[word][self.labels.index(label)] =\
                        (table[word][self.labels.index(label)] + self.alpha) /\
                        (V+L[label])

        return None

    def predict(self, X: list) -> dict:
        """ Perform classification on an array of test vectors X. """

        predictions = {}
        for line in X:
            predictions[line] = [i for i in self.p_labels]
            words = line.split()
            for word in words:
                if word in self.chance:
                    for i in range(len(self.labels)):
                        predictions[line][i] += math.log(self.chance[word][i])

            for i in range(len(self.labels)):
                if predictions[line][i] == max(predictions[line]):
                    predictions[line] = self.labels[i]
                    break
        return predictions

    def score(self, X_test: list, y_test: list) -> float:
        """ Returns the mean accuracy on the given test data and labels. """

        test = self.predict(X_test)
        correct = 0
        testdict = {}

        for line, label in zip(X_test, y_test):
            testdict[line] = label

        for line in X_test:
            if test[line] == testdict[line]:
                correct += 1
        return correct / len(y_test)
