"""hasky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path
from django.views.generic.detail import DetailView
from hasky.settings import DEBUG
from haskyApp import views

urlpatterns = [
    path("logout", views.logout, name="logout"),
    path('vote/', views.vote, name="Vote"),

    path('admin/', admin.site.urls),
    path('', views.index, name = 'new'),
    path('new', views.index, name = 'new'),
    path('hot', views.hot, name = 'hot'),
    path('questions/<int:pk>', views.question, name = 'questions'),
    path('signup', views.signup, name = 'signup'),
    path('login', views.login, name = 'login'),
    path("h'ask", views.ask, name = 'ask'),
    path('tags/<int:pk>', views.tag, name = 'tags'),
    path('profile/edit', views.edit, name = 'edit')
    #path('questions/<int:pk>', views.one_question.as_view(), name = 'questions')
]  
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)