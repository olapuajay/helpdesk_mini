from django.urls import path
from . import views_frontend

urlpatterns = [
    path("register/", views_frontend.register_view, name="register"),
    path("login/", views_frontend.login_view, name="login"),
    path("logout/", views_frontend.logout_view, name="logout"),
]
