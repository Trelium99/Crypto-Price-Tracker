from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("crypto-info/<slug:slug>", views.info, name="info")
]