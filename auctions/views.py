from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Project, User, Language, Comment
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import User


import requests
from django.conf import settings
from django.shortcuts import redirect, render

# GitHub-a yönləndir
def github_login(request):
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&scope=repo"
    )
    return redirect(github_auth_url)

# Callback: Access token al
def github_callback(request):
    code = request.GET.get("code")
    token_url = "https://github.com/login/oauth/access_token"

    response = requests.post(
        token_url,
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )
    access_token = response.json().get("access_token")
    request.session["github_token"] = access_token
    return redirect("github_repos")

# Reposları göstər
def github_repos(request):
    token = request.session.get("github_token")
    if not token:
        return redirect("github_login")

    url = "https://api.github.com/user/repos"
    response = requests.get(url, headers={"Authorization": f"token {token}"})
    repos = response.json()

    return render(request, "repos.html", {"repos": repos})

def index(request):
    projects = Project.objects.all()
    return render(request, "auctions/index.html", {
        "projects": projects
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
languages = [
    {"name": "Python"},
    {"name": "JavaScript"},
    {"name": "Java"},
    {"name": "C#"},
    {"name": "Ruby"},
    {"name": "PHP"},
    {"name": "C++"},
    {"name": "Swift"},
    {"name": "Go"},
    {"name": "Kotlin"}
]
def my_projects(request):
    
    return render(request, "auctions/my_projects.html")
def project(request, project_id):
    # Here you would typically fetch the project details from the database
    # For now, we will just render a placeholder template
    return render(request, "auctions/project.html", {
        "project_id": project_id
    })

def favorite_projects(request):
    # Here you would typically fetch the user's favorite projects from the database
    # For now, we will just render a placeholder template
    return render(request, "auctions/favorite_projects.html")
from django.shortcuts import render, redirect
from .models import Project, Language

def create_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        selected_languages = request.POST.getlist("languages")
        author = request.user
        code= request.POST.get("code", "")

        # project yarat
        new_project = Project.objects.create(
            title=title,
            description=description,
            author=author,
            code=code
        )

        # seçilmiş dilləri ManyToManyField-ə əlavə et
        new_project.languages.set(selected_languages)

        # uğurlu olduqdan sonra index səhifəsinə yönləndir
        return redirect("index")   # burada "index" urls.py-də verdiyin name-dir

    # GET zamanı: bütün dilləri template-ə göndər
    languages = Language.objects.all()
    return render(request, "auctions/create_project.html", {"languages": languages})
def view_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status=404)

    return render(request, "auctions/view_project.html", {
        "project": project
    })