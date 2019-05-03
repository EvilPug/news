from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from accounts.models import User
from news.models import NewsModel
from news.scraputils import get_news
from news.bayes import NaiveBayesClassifier


def index(request):

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)

        if user.news_labeled != '':
            labels = set(user.news_labeled.split(" "))
            ids = [i.split(':')[0] for i in list(labels)]
            rows = NewsModel.objects.exclude(pk__in=ids)
            fav = set(int(id) for id in user.favorite.split(" "))
        else:
            rows = NewsModel.objects.all()
            fav = []
        count = len(rows)
        return render(request, 'news/index.html',
                      {'rows': rows, 'count': count, 'fav:': fav})

    else:
        rows = NewsModel.objects.all()

    count = len(rows)
    return render(request, 'news/index.html',
                  {'rows': rows, 'count': count})


@login_required
def add_label(request):
    if request.POST:
        user = User.objects.get(username=request.user)
        if user.news_labeled == "":
            user.news_labeled = request.POST['label']

        user.news_labeled += " " + request.POST['label']
        user.save()
    return redirect('/')


@login_required
def add_favorite(request):
    if request.POST:
        user = User.objects.get(username=request.user)
        if user.favorite == "":
            user.favorite = request.POST['favorite']

        user.favorite += " " + request.POST['favorite']
        user.save()
    return redirect('/')


@login_required
def favorite(request):
    user = User.objects.get(username=request.user)

    if user.news_labeled != '':
        ids = set(user.favorite.split(" "))
        fav_news = NewsModel.objects.filter(pk__in=ids)
    else:
        fav_news = ['Nothing to see here']

    return render(request, 'news/favorite.html',
                  {'fav_news': fav_news})


@login_required
def update_news(request):
    rows = NewsModel.objects.all()
    n_pages = int(request.POST['n_pages'])
    update_list = get_news("https://news.ycombinator.com/newest",
                           n_pages=n_pages)
    url_list = [row.url for row in rows]

    for news in list:
        if news[2] not in url_list:
            s = NewsModel(title=news[0],
                          author=news[1],
                          url=news[2],
                          comments=news[3],
                          points=news[4])
            s.save()

    print('News added:', len(update_list))
    return redirect('/', {'rows': rows})


@login_required
def recommendations(request):
    classifier = NaiveBayesClassifier()
    n_labels = User.objects.get(username=request.user).news_labeled
    good = maybe = never = []

    if n_labels != '':
        labels = set(n_labels.split(" "))
        ids = [i.split(':')[0] for i in list(labels)]
        y_train = [i.split(':')[1] for i in list(labels)]

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

        good = {'news': good, 'count': len(good)}
        maybe = {'news': maybe, 'count': len(maybe)}
        never = {'news': never, 'count': len(never)}

    else:
        good = maybe = never = ['Go label some news!']

    return render(request, 'news/recommendations.html',
                  {'good': good, 'maybe': maybe, 'never': never})
