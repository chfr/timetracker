from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url('^login/$', auth_views.login, name="user_login"),
    url('^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='user_logout'),
    url('^password_change/$', auth_views.password_change, name='user_password_change'),
    url('^password_change/done/$', auth_views.password_change_done, name='user_password_change_done'),
    url('^password_reset/$', auth_views.password_reset, name='user_password_reset'),
    url('^password_reset/done/$', auth_views.password_reset_done, name='user_password_reset_done'),
    url('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='user_password_reset_confirm'),
    url('^reset/done/$', auth_views.password_reset_complete, name='user_password_reset_complete'),

    url(r'^$', views.index, name='index'),
    url(r'^tasks/?$', views.tasks, name='tasks'),
    url(r'^task/(?P<slug>\S+)/?$', views.task, name='task'),
    url(r'^spans/?$', views.spans, name='spans'),
    url(r'^span/(?P<span_id>\d+)/?$', views.span, name='span'),
    url(r'^settings/?$', views.settings, name='settings'),
]
