import csv
import math
import string
import collections


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


with open('static/SMSSpamCollection.txt', encoding='utf-8') as f:
    data = list(csv.reader(f, delimiter="\t"))
X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [clean(x).lower() for x in X]
X_train, y_train, X_test, y_test = X[0:3900], y[0:3900], X[3900:], y[3900:]


#X = ['i love this sandwich', 'This is an amazing place', 'I feel very good about these beers', 'This is my best work', 'What an awesome view', 'I do not like this restaurant', 'I am tired of this stuff', 'I can’t deal with this', 'He is my sworn enemy', 'My boss is horrible']
#y = ['Positive','Positive','Positive','Positive','Positive','Negative','Negative','Negative','Negative','Negative']
#X = [clean(x).lower() for x in X]

labels = [i for i in set(y)]
labels.sort()
amount = len(labels)



dict = [[] for l in range(len(X))]
for i in range(len(X)):
    dict[i] = [X[i], y[i]]

print(dict[0][1])


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



print(len(dict))
print(len(X))
print(counter)


#log Dc/D
D = len(dict)
p_labels = [math.log(counter[label] / D) for label in labels]
print(p_labels)


#Количество уникальных слов
V = len(table)
print(V)


L = {}
for label in labels:
    L[label] = 0
    for word in table:
        L[label] += table[word][labels.index(label)]
print(L)


chance = {}
alpha = 1
for num in range(len(X)):
    string = X[num]
    string = string.split()

    for word in string:
        chance[word] = [label for label in labels]
        for label in labels:
            chance[word][labels.index(label)] = (table[word][labels.index(label)] + alpha)/(V+L[label])









def lll():
    list = {}
    for line in X:
        list[line] = [i for i in p_labels]

        words = line.split()
        for word in words:
            if word in chance:
                for i in range(amount):
                    list[line][i] += math.log(chance[word][i])
    print(list)
    return None

lll()



"""
def predict(X):
    labels = []
    classes = len(labels)
    for string in X:
        string_labels = [i for i in p_labels]
        words = string.split()
        for word in words:
            if word in table[0]:
                for i in range(classes):
                    string_labels[i] += math.log(table[i + classes + 1][table[0].index(word)])
        for i in range(classes):
            if string_labels[i] == max(string_labels):
                labels.append(labels[i])
                break
    return labels


predict(X)
"""





#
