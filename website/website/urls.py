"""
URL configuration for website project.

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
from django.urls import path
from game import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/create', views.create_game, name='create_game'),
    path('game/', views.choose_player, name='choose_player'),
    path('game/display/<str:player_tag>/', views.play_game, name='play_game'),
    path('game/move/<str:player_tag>/<str:direction>', views.move_player, name='move_player'),
]
