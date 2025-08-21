from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("my_projects", views.my_projects, name="my_projects"),
    path("project/<int:project_id>", views.project, name="project"),
    path("create_project", views.create_project, name="create_project"),
    path("view_project/<int:project_id>", views.view_project, name="view_project"),
    path("github/login/", views.github_login, name="github_login"),
    path("github/callback/", views.github_callback, name="github_callback"),
    path("github/repos/", views.github_repos, name="github_repos"),
]