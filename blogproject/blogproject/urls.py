"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from blog_app import views as bviews
from django.conf.urls.static import static
from groups import views as gviews
from posts import views as pviews


urlpatterns = [
    path('',bviews.BlogListView.as_view(),name='index'),
    #path('',views.BlogListView.as_view(),name='index'),
    path('admin/', admin.site.urls),
    path('blog_app/',include('blog_app.urls',namespace='blog_app')),
    path('groups/',include('groups.urls',namespace='groups')),
    path('posts/',include('posts.urls',namespace='posts')),
    path('logout/',bviews.user_logout,name='logout'),
    path('special/',bviews.special, name='special')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
