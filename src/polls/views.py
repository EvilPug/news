import time
import hashlib
import requests
from .models import NewsModel, Users
from .scraputils import get_news
from .bayes import NaiveBayesClassifier
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect



def index(request):
    # import pdb; pdb.set_trace()
    rows = NewsModel.objects.filter(label=None)
    count = len(rows)
    return render(request, 'index.html', {'rows': rows, 'count': count})


def admin(request):
    user = request.session['username']
    news = NewsModel.objects.exclude(label=None)

    list = ''
    for new in news:
        list += ' ' + str(new.id)+':'+new.label
    print(list)
    return HttpResponse("Admin panel here")

def signup(request):
    if request.POST:
        users = Users.objects.all()
        username = request.POST['username']
        for user in users:
            if user.username == username:
                return HttpResponse("User alredy exist!")
            else:
                if len(username) <= 20:
                    encode = request.POST['password'].encode()
                    hashed_pass = hashlib.md5(encode).hexdigest()
                    u = Users(username = username,
                              password = hashed_pass)
                    u.save()


                    print("New user: ", username)
                    return redirect('/')
                else:
                    return HttpResponse("Username max_length is 20")
    return render(request, 'signup.html')

def login(request):

    try:
        user = Users.objects.get(username=request.session['username'])
        if request.session['password'] == user.password:

            if user.news_labeled != '':
                labels = set(user.news_labeled.split(" "))
                ids = []
                for i in list(labels):
                    ids += [i.split(':')[0]]

                rows = NewsModel.objects.exclude(pk__in=ids)
            else:
                rows = NewsModel.objects.all()

            count = len(rows)
            return render(request,
                          'index.html',
                          {'rows': rows,
                           'count': count,
                           'user':request.session['username']
                          }
                         )
        else:
            return render(request, 'login.html')
    except KeyError:
        pass

    if request.POST:
        try:
            user = Users.objects.get(username=request.POST['username'])
            hashed = hashlib.md5(request.POST['password'].encode()).hexdigest()

            if hashed == user.password:
                request.session['username'] = user.username
                request.session['password'] = hashed

                labels = set(user.news_labeled.split(" "))
                ids = []
                for i in list(labels):
                    ids += [i.split(':')[0]]

                rows = NewsModel.objects.exclude(pk__in=ids)
                count = len(rows)
                return render(request,
                              'index.html',
                              {'rows': rows,
                               'count': count,
                               'user':request.session['username']
                              }
                             )

        except Users.DoesNotExist:
            return HttpResponse("Login or password invalid")
    return render(request, 'login.html')

@login_required
def logout(request):
    try:
        del request.session['username']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponse("Logged out")

@login_required
def add_label(request):
    rows = NewsModel.objects.filter(label=None)

    if request.POST:
        user = request.session['username']
        add = Users.objects.get(username=user)
        if add.news_labeled == "":
            add.news_labeled = request.POST['label']

        add.news_labeled += " " + request.POST['label']
        add.save()
    return redirect('/', {'rows': rows})

@login_required
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

@login_required
def recommendations(request):
    classifier = NaiveBayesClassifier()
    user = request.session['username']
    n_labels = Users.objects.get(username=user).news_labeled

    good = []
    maybe = []
    never = []

    if n_labels != '':
        labels = set(n_labels.split(" "))
        ids = []
        y_train = []
        for i in list(labels):
            ids += [i.split(':')[0]]
            y_train += [i.split(':')[1]]

        rows = NewsModel.objects.filter(pk__in=ids)


        X_train = [row.title for row in rows]

        classifier.fit(X_train, y_train)

        unlabeled_rows = NewsModel.objects.all()
        x = [row.title for row in unlabeled_rows]
        predicted = classifier.predict(x)

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
    else:
        good = ['Go label some news!']
        maybe = ['Go label some news!']
        never = ['Go label some news!']
    return render(request, 'test.html',
                  {'good': good, 'maybe': maybe, 'never': never})


@login_required
def favorite(request):

    user = Users.objects.get(username=request.session['username'])
    print(user)
    labels = set(user.favorite.split(" "))

    fav_news = NewsModel.objects.filter(pk__in=labels)
    return render(request, 'favorite.html', {'fav_news': fav_news})
