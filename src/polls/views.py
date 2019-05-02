from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from accounts.models import User
from polls.models import NewsModel
from polls.scraputils import get_news
from polls.bayes import NaiveBayesClassifier




def index(request):
    # import pdb; pdb.set_trace()
    if request.user != 'AnonymousUser':
        user = User.objects.get(username=request.user)
        labels = set(user.news_labeled.split(" "))
        ids = []
        for i in list(labels):
            ids += [i.split(':')[0]]

        rows = NewsModel.objects.exclude(pk__in=ids)
    else:
        rows = NewsModel.objects.all()
    count = len(rows)
    return render(request, 'polls/index.html', {'rows': rows, 'count': count})

@login_required
def add_label(request):

    if request.POST:
        add = User.objects.get(username=request.user)
        if add.news_labeled == "":
            add.news_labeled = request.POST['label']

        add.news_labeled += " " + request.POST['label']
        add.save()
    return redirect('/')

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
    n_labels = User.objects.get(username=request.user).news_labeled

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
        good = {'news':good, 'count': len(good)}
        maybe = {'news':maybe, 'count': len(maybe)}
        never = {'news':never, 'count': len(never)}
    else:
        good = ['Go label some news!']
        maybe = ['Go label some news!']
        never = ['Go label some news!']
    return render(request, 'polls/recommendations.html',
                  {'good': good, 'maybe': maybe, 'never': never})


@login_required
def favorite(request):

    user = User.objects.get(username=request.user)
    print(user)
    labels = set(user.favorite.split(" "))

    fav_news = NewsModel.objects.filter(pk__in=labels)
    return render(request, 'polls/favorite.html', {'fav_news': fav_news})
