from django.urls import path,re_path

from . import views as gviews

app_name = 'groups'

urlpatterns = [
    path("", gviews.ListGroups.as_view(), name="groups"),
    re_path(r"^new/$", gviews.CreateGroup.as_view(), name="create"),
    re_path(r"^posts/in/(?P<slug>[-\w]+)/$",gviews.SingleGroup.as_view(),name="single"),
    re_path(r"join/(?P<slug>[-\w]+)/$",gviews.JoinGroup.as_view(),name="join"),
    re_path(r"leave/(?P<slug>[-\w]+)/$",gviews.LeaveGroup.as_view(),name="leave"),
]