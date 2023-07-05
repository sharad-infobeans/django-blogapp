from django.urls import path ,re_path
from blog_app import views


app_name = 'blog_app'

urlpatterns=[
    path('',views.BlogListView.as_view(),name='blogs'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='detail'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    re_path(r'^create/$', views.BlogCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.BlogDeleteView.as_view(), name='delete'),
]