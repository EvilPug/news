import csv
import math
import string
import collections


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


with open('SMSSpamCollection.txt', encoding='utf-8') as f:
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


"""
for num in range(1):
    string = X[num]
    string = string.split()
    chance = {}
    alpha = 1
    for word in string:
        chance[word] = [label for label in labels]
        for label in labels:
            chance[word][labels.index(label)] = (table[word][labels.index(label)] + alpha)/(V+L[label])
    print(chance)
"""

print(p_labels)
for line in X[:3]:
    line_l = [i for i in p_labels]
    words = line.split()
    p_label_list = p_labels
    for word in words:
        for i in range(amount):
            if word in chance:
                line_l[i] += math.log(chance[word][i])
                print(math.log(chance[word][i]))
    print(line_l)
    for i in range(amount):
        if line_l[i] == max(line_l):
            labels.append(labels[i])
            break
print(labels)


"""
        for k, v in p_label_list.items():
                if v == maximum:
                    print((num+1), k)


    maximum = max(p_label_list.values())
    for k, v in p_label_list.items():
            if v == maximum:
                print((num+1), k)
"""


#Переработать L
#Дописать if not in (если слова не было в обучающей выборке)



#print(X[0])
#print(X[0].split())
#print(table)
