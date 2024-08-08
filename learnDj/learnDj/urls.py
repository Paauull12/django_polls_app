"""
URL configuration for learnDj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views_contrib
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views
from users_auth import views as views_auth

urlpatterns = [
    path('', include("polls.urls")),
    path('nothing/', views.home, name='home'),
    path('register/', views_auth.register, name='register_users'),
    path('login/', auth_views_contrib.LoginView.as_view(template_name="users_auth/login.html"), name='login_users'),
    path('logout/', auth_views_contrib.LogoutView.as_view(template_name="users_auth/logout.html"), name='logout_users'),
    path('admin/', admin.site.urls),
    path('profile/', views_auth.profile, name='profile'),
] + debug_toolbar_urls()
