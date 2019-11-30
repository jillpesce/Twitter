from django.shortcuts import render, redirect
from core.models import Post, Hashtag
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def home(request):
    if request.method == "POST":
        body = request.POST["body"]
        post = Post.objects.create(body=body, author=request.user)
        parse_body(post)
        Post.objects.all().order_by('-date')
        return redirect("/home")
    else:
        posts = Post.objects.all()
        hashtags = Hashtag.objects.all()
    return render(request, "home.html", {"posts": posts, "hashtags": hashtags})

def profile(request):
    post = Post.objects.get(id=request.GET['id'])
    author = post.author
    posts = Post.objects.filter(author=author)
    return render(request, "profile.html", {"posts": posts, "author": author})

def hashtag(request, name):
    hashtag = Hashtag.objects.get(name=name)
    posts = hashtag.posts.all()
    return render(request, "hashtag.html", {"hashtag": hashtag, "posts": posts})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home/")
    return render(request, "login.html", {})

def logout_view(request):
    logout(request)
    return redirect("/")

def like_view(request):
    post = Post.objects.get(id=request.GET['id'])
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else: 
        post.likes.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def signup_view(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        login(request, user)
        return redirect('/home')
    return render(request, 'login.html', {})

def delete_view(request):
    post = Post.objects.get(id=request.GET['id'])
    post.delete()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def parse_body(post):
    hashtags = [s[1:] for s in post.body.split(" ") if s.startswith("#")]
    for s in hashtags:
        for h in Hashtag.objects.all():
            if s == h.name:
                h.posts.add(post)
                print("BREAK")
                break
        else:
            h = Hashtag.objects.create(name=s)
            h.posts.add(post)
            print("NEW HASH: " + str(post))