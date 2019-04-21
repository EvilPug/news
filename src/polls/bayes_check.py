import csv
import string
from bayes import NaiveBayesClassifier


def clean(s: str) -> str:
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


with open('static/SMSSpamCollection.txt', encoding='utf-8') as f:
    data = list(csv.reader(f, delimiter="\t"))

X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [clean(x).lower() for x in X]

p = 70
train = int((len(X)/100)*p)
X_train, y_train, X_test, y_test = X[0:train], y[0:train], X[train:], y[train:]

model = NaiveBayesClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
