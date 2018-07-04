from django.conf.urls import url
from .api import LoginView,LogoutView,IsLoogedIntView

urlpatterns =[
   url(r'^login/$', LoginView.as_view()),
   url(r'^logout/$',LogoutView.as_view()),
   url(r'^lslogin/$',IsLoogedIntView.as_view()),

]

