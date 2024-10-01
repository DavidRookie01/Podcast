from django.http import JsonResponse, HttpResponse
from django.shortcuts  import render
import modules.database_utils as du

def loadmain(request):
    return render(request, "myapp/podcast.html")

def load_podcast(request):
    con, cursor = du.db_connect('postgres')
    cursor.execute("select title, date, link, series_name, keywords, podcast_id from public.podcast_transcripts")
    podcasts = cursor.fetchall()
    con.close()
    return JsonResponse({'podcasts': podcasts})

def searchPodcasts(request):
    query = request.GET.get('query')
    con, cursor = du.db_connect('postgres')
    query = '%' + query + '%'
    cursor.execute("select title, date, link, series_name, keywords, podcast_id from public.podcast_transcripts where podcast_id ilike %s", [query])
    podcasts = cursor.fetchall()
    con.close()
    return JsonResponse({'podcasts': podcasts})
    