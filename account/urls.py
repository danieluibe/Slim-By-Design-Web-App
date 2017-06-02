from django.conf.urls import url
from account import views

urlpatterns =          [url(r'^$', views.login, name='login'),
                       url(r'^login/$', views.login, name='login'),
                       # url(r'^register/$', views.register, name='register'),
                       #url(r'^index/$', views.table, name='index'),
                       url(r'^logout/$', views.logout, name='logout'),
                       # url(r'^ErrorMessageAfterLogin/$', views.ErrorMessageAfterLogin, name='ErrorMessageAfterLogin'),
                       url(r'^filter/$', views.filter, name = 'filter'),
                       url(r'^table/$', views.table, name = 'table'),
                       # url(r'^graph/$', views.graph, name='graph'),
                       url(r'^restaurant/$', views.restaurant, name = 'restaurant'),
                       url(r'^restaurant_csv/$', views.restaurant_csv, name = 'restaurant_csv'),
                       url(r'^review/$', views.review, name = 'review'),
                       url(r'^review_csv/$', views.review_csv, name = 'review_csv'),
                       url(r'^home/$', views.home, name = 'home'),
                       url(r'^home_csv/$', views.home_csv, name = 'home_csv'),

                       ]