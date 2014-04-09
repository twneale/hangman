from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^new_game/$', 'app.views.new_game', name='new_game'),
    url(r'^resume_game/(?P<game_id>\d+)/$', 'app.views.resume_game', name='resume_game'),
    url(r'^play/$', 'app.views.game', name='game'),
    url(r'^game_json/$', 'app.views.game_json', name='game_json'),
    url(r'^victory/$', 'app.views.victory', name='victory'),
    url(r'^failure/$', 'app.views.failure', name='failure'),
)
