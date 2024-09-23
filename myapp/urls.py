from django.urls import path
from myapp.views import podcast
from django.urls import path


urlpatterns = [
    path('', podcast.loadmain, name='loadmain'),  
    path('load_podcast/', podcast.load_podcast, name='load_podcast'),
]

