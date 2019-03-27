import hashlib
import time
from .models import NewsModel, Users
from .scraputils import get_news
from .bayes import NaiveBayesClassifier
from django.shortcuts import render, HttpResponse, redirect



def index(request):
    # import pdb; pdb.set_trace()
    rows = NewsModel.objects.filter(label=None)
    count = len(rows)
    return render(request, 'index.html', {'rows': rows, 'count': count})


def admin(request):
    return HttpResponse("Admin panel here")

def signup(request):
    if request.POST:
        users = Users.objects.all()
        for user in users:
            if user.username == request.POST['username']:
                return HttpResponse("User alredy exist!")
            else:
                if len(request.POST['username']) <= 20:
                    encode = request.POST['password'].encode()
                    hashed_pass = hashlib.md5(encode).hexdigest()
                    u = Users(username = request.POST['username'],
                              password = hashed_pass)
                    u.save()
                    print("New user: ", request.POST['username'])
                    return redirect('/')
                else:
                    return HttpResponse("Username max_length is 20")
    return render(request, 'signup.html')

def login(request):
    rows = NewsModel.objects.filter(label=None)
    count = len(rows)

    if request.POST:
        users = Users.objects.all()
        l = request.get_full_path()
        print(l)
        username = request.POST['username']
        password = request.POST['password'].encode()
        h = hashlib.md5(password).hexdigest()

        for user in users:
            if user.username == username and h == user.password:
                return render(request, 'index.html', {'rows': rows, 'count': count})
            else:
                return HttpResponse("Login or password incorrect")
    return render(request, 'login.html')

def add_label(request):
    rows = NewsModel.objects.filter(label=None)
    if request.POST:
        row = request.POST['label']
        label = request.POST['label'].split(' ')[0]
        id = request.POST['label'].split(' ')[1]
        change = NewsModel.objects.get(id=id)
        change.label = label
        change.save()
    return redirect('/', {'rows': rows})


def update_news(request):
    rows = NewsModel.objects.all()
    n = int(request.POST['n_pages'])
    list = get_news("https://news.ycombinator.com/newest", n_pages=n)
    update_list = []
    url_list = [row.url for row in rows]

    for news in list:
        if news[2] not in url_list:

            s = NewsModel(title=news[0],
                         author=news[1],
                         url=news[2],
                         comments=news[3],
                         points=news[4],
                         label = None)

            s.save()
            print(s.id, s.title)
    return redirect('/', {'rows': rows})


def recommendations(request):
    classifier = NaiveBayesClassifier()
    rows = NewsModel.objects.exclude(label=None)
    X_train = [row.title for row in rows]
    y_train = [row.label for row in rows]
    classifier.fit(X_train, y_train)

    unlabeled_rows = NewsModel.objects.filter(label=None)
    x = [row.title for row in unlabeled_rows]
    predicted = classifier.predict(x)

    good = []
    maybe = []
    never = []
    print(len(unlabeled_rows))

    try:
        for i in range(len(unlabeled_rows)):
            if list(predicted.values())[i] == '0':
                never.append(unlabeled_rows[i])
            elif list(predicted.values())[i] == '1':
                maybe.append(unlabeled_rows[i])
            elif list(predicted.values())[i] == '2':
                good.append(unlabeled_rows[i])
    except IndexError:
        print('Percentage of predicted news: ',
              len(predicted.values())/len(unlabeled_rows))

    return render(request, 'recommendations.html',
                  {'good': good, 'maybe': maybe, 'never': never})
