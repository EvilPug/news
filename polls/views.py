from django.shortcuts import render, HttpResponse, redirect
from .scraputils import get_news
from .db import News, session, save
from .models import NewsModel

from .bayes import NaiveBayesClassifier


def index(request):
    #import pdb; pdb.set_trace()
    rows = NewsModel.objects.filter(label=None)
    count = len(rows)
    return render(request, 'index.html', {'rows': rows, 'count': count})


def admin(request):
    return HttpResponse("Admin panel here")


def add_label(request):
    rows = NewsModel.objects.filter(label=None)
    if request.POST:
        row = request.POST['label']
        label = request.POST['label'].split(' ')[0]
        id = request.POST['label'].split(' ')[1]
        change = NewsModel.objects.get(id=id)
        change.label=label
        change.save()
    return redirect('/', {'rows': rows})

def update_news(request):
    rows = NewsModel.objects.all()
    n = request.POST['n_pages']
    n = int(n)
    list = get_news("https://news.ycombinator.com/newest", n_pages=n)
    update_list = []

    url_list = [row.url for row in rows]

    for news in list:
        if news[2] not in url_list:
            print(news[0])
            update_list.append(news)
    save(update_list)
    return redirect('/', {'rows': rows})


def recommendations(request):
	s = session()
	classifier = NaiveBayesClassifier()
	
	labeled_news = s.query(News).filter(News.title not in x_train and News.label != None).all()
	X_train = [row.title for row in recently_marked_news]
	y_train = [row.label for row in recently_marked_news]
	classifier.fit(X_train, y_train)
	
	blank_rows = s.query(News).filter(News.label == None).all()
	X = [row.title for row in blank_rows]
	labels = classifier.predict(X)
	good = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == '2']
	maybe = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == '1']
	never = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == '0']
	
	return render(request, 'recommendations.html', {'good': good, 'maybe':maybe, 'never': never})

