from django.shortcuts import render, redirect
from core.models import Post, Hashtag
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    if request.method == "POST":
        body = request.POST["body"]
        post = Post.objects.create(body=body, author=request.user)
        parse_body(post)
        return redirect("/home")
    else:
        posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})

def profile(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user)
    else:
        posts = []
    return render(request, "profile.html", {"posts": posts})

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

def signup_view(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        login(request, user)
        return redirect('/home')
    return render(request, 'login.html', {})

def delete_view(request):
    post = Post.objects.get(id=request.GET['id'])
    post.delete()
    return redirect('/home/')

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