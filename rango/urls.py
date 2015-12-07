from django.conf.urls import patterns, url
from rango import views

urlpatterns = [
    url(r'^$', views.tempo, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.tempo, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.tempo, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.tempo, name='add_page'),
    #url(r'^register/$', views.tempo, name='register'),
    #url(r'^login/$', views.tempo, name='login'),
    #url(r'^logout/$', views.tempo, name='logout'),
    url(r'^restricted/', views.tempo, name='restricted'),
    url(r'^search/', views.tempo, name='search'),
    url(r'^goto/$', views.tempo, name='goto'),
    url(r'^like_category/$', views.tempo, name='like_category'),
    url(r'^suggest_category/$', views.tempo, name='suggest_category'),

]
# urlpatterns = patterns('',
#     url(r'^$', views.index, name='index'),
#     url(r'^about/$', views.about, name='about'),
#     url(r'^add_category/$', views.add_category, name='add_category'),
#     url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
#     url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
#     #url(r'^register/$', views.register, name='register'),
#     #url(r'^login/$', views.user_login, name='login'),
#     #url(r'^logout/$', views.user_logout, name='logout'),
#     url(r'^restricted/', views.restricted, name='restricted'),
#     url(r'^search/', views.search, name='search'),
#     url(r'^goto/$', views.track_url, name='goto'),
#     url(r'^like_category/$', views.like_category, name='like_category'),
#     url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
#     )