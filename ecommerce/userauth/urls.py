from django.urls import path
from userauth import views

app_name = "userauth"

urlpatterns = [
    path("signup/", views.register_view, name="signup"),
    path("signin/", views.login_view, name="signin"),
    path("logout/", views.logout_view, name="logout"),
]   
