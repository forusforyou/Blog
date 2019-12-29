from django.shortcuts import render, HttpResponse, redirect
from user.models import User, Article, Comment
from blog.utils import md5_encryption
# Create your views here.


def auth(func):
    def inner(*args, **kwargs):
        request = args[0]
        if request.session.get('user'):
            res = func(*args, **kwargs)
            return res
        else:
            return redirect('/login/')
    return inner


def login(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('user', '')
        pwd = request.POST.get('pwd', '')
        print(user, pwd)
        if user and pwd:
            try:
                user = User.objects.all().get(user=user)
            except Exception as e:
                return redirect('/login/')

            if md5_encryption(pwd) == user.pwd:
                request.session['user'] = user.user
                return redirect('/index/')
        return render(request, 'login.html')


def register(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        if user and pwd:
            user = User(user=user, pwd=md5_encryption(pwd))
            user.save()
            return render(request, 'login.html')
        else:
            return HttpResponse('用户名或者密码不能为空')


@auth
def index(request, *args, **kwargs):
    content = Article.objects.all().values('pk', 'title', 'user__user', 'create_time')
    return render(request, 'index.html', {"content": content})


@auth
def add_article(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'add_article.html')
    else:
        content = request.POST.get('content')
        title = request.POST.get('title')
        user = User.objects.get(user=request.session['user'])
        import datetime
        create_time = datetime.datetime.now()
        article = Article(content=content, title=title, create_time=create_time, user=user)
        article.save()
        return redirect('/index/')


@auth
def delete_article(request, pk):
    try:
        Article.objects.get(pk=pk).user_set.get(user=request.session['user'])
    except Exception as e:
        return HttpResponse('无权限')

    Article.objects.get(pk=pk).delete()
    return HttpResponse('删除成功')


@auth
def article(request, pk):
    if request.method == 'GET':
        try:
            article = Article.objects.get(pk=pk)
        except Exception as e:
            return HttpResponse('文章不存在')
        comments = article.comment_set.all()
        HasPermit = '' if article.user.user == request.session['user'] else 'disabled'
        return render(request, 'article.html', {"article": article, "Permit": HasPermit,"Comment": comments})
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            article = Article.objects.get(pk=pk)
            article.title = title
            article.content = content
            article.save()
            return redirect('/index/')

@auth
def comment(request):
    if request.method == 'GET':
        pass
    else:
        import datetime
        article_id = request.POST.get('artpk')
        print(article_id)
        content = request.POST.get('content')
        print(request.POST)
        create_time = datetime.datetime.now()
        user = User.objects.all().get(user=request.session['user'])
        try:
            article = Article.objects.get(pk=article_id)
        except Exception as e:
            return HttpResponse('文章不存在')

        com = Comment(user=user, article=article, create_time=create_time, content=content)
        com.save()
        # print(request.path)
        return redirect('/article/' + article_id + '/')