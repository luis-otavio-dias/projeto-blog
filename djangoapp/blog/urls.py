from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post, name="post"),
    path("page/<slug:slug>", views.page, name="page"),
    path("created_by/<int:author_pk>", views.created_by, name="created_by"),
    path("category/<slug:slug>", views.category, name="category"),
]
