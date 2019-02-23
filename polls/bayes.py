import math
import collections

class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.labels = []
        self.table = []
        self.p_labels = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        labels = [i for i in set(y)]
        labels.sort()
        amount = len(labels)

        dict = [[] for l in range(len(X))]
        for i in range(len(X)):
            dict[i] = [X[i], y[i]]

        table = {}
        for i in range(len(X)):
            words = X[i].split()
            for word in words:
                if word not in table:
                    table[word] = [0]*amount
                if dict[i][1] == labels[0]:
                    table[word][0] += 1
                elif dict[i][1] == labels[1]:
                    table[word][1] += 1
                elif dict[i][1] == labels[2]:
                    table[word][2] += 1
                elif dict[i][1] == labels[3]:
                    table[word][3] += 1
                elif dict[i][1] == labels[4]:
                    table[word][4] += 1

        for i in range(amount):
            counter = collections.Counter()
            for j in dict:
                counter[j[1]] += 1

        #log (Dc/D)
        D = len(dict)
        p_labels = [math.log(counter[label] / D) for label in labels]

        #Количество уникальных слов
        V = len(table)

        #Cуммарное количество слов по классам (label)
        L = {}
        for label in labels:
            L[label] = 0
            for word in table:
                L[label] += table[word][labels.index(label)]




    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        for line in X:
            line_l = [i for i in p_labels]
            words = line.split()
            p_label_list = p_labels
            for word in words:
                for i in range(amount):
                    if word in chance:
                        line_l[i] += math.log(chance[word][i])

            maximum = max(line_l)
            for i in range(amount):
                if line_l[i] == maximum:
                    predicted += v
        return predicted



    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = 0
        for i, data in enumerate(X_test):
            if self.predict(data) == y_test[i]:
                count += 1

        return count / len(X_test)
