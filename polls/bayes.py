import math
import collections

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.chance = {}
        self.p_labels = []
        self.amount = 0
        self.labels = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [i for i in set(y)]
        self.labels.sort()
        self.amount = len(self.labels)

        dict = [[] for l in range(len(X))]
        for i in range(len(X)):
            dict[i] = [X[i], y[i]]

        table = {}
        
        for i in range(len(X)):
            words = X[i].split()
            for word in words:
                table[word] = [0]*self.amount

        for k in range(self.amount):
            for i in range(len(X)):
                words = X[i].split()
                for word in words:
                    if dict[i][1] == self.labels[k]:
                        table[word][k] += 1
        print(table)


        for i in range(self.amount):
            counter = collections.Counter()
            for j in dict:
                counter[j[1]] += 1
        #log (Dc/D)
        D = len(dict)
        self.p_labels = [math.log(counter[label] / D) for label in self.labels]



        #Количество уникальных слов
        V = len(table)

        #Cуммарное количество слов по классам (label)
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
                    self.chance[word][self.labels.index(label)] = (table[word][self.labels.index(label)] + self.alpha)/(V+L[label])


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """

        list = {}
        for line in X:
            list[line] = [i for i in self.p_labels]
            words = line.split()
            for word in words:
                if word in self.chance:
                    for i in range(len(self.labels)):
                        list[line][i] += math.log(self.chance[word][i])

            for i in range(len(self.labels)):
                if list[line][i] == max(list[line]):
                    list[line] = self.labels[i]
                    break
        return list


    def score(self, X_test, y_test):
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

if __name__ == '__main__':
    print('OK')
