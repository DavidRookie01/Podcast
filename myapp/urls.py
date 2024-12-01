from django.urls import path
from myapp.views import podcast
from django.urls import path


urlpatterns = [
    path('', podcast.loadmain, name='loadmain'),  
    path('load_podcast/', podcast.load_podcast, name='load_podcast'),
    path('searchPodcasts/', podcast.searchPodcasts, name='searchPodcasts'),
    path('load_result/', podcast.load_result, name='load_result'),
    path('update_feedback_positive/', podcast.update_feedback_positive, name='update_feedback_positive'),
    path('update_feedback_negative/', podcast.update_feedback_negative, name='update_feedback_negative'),
]


