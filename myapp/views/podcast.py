from django.http import JsonResponse, HttpResponse
from django.shortcuts  import render
import modules.database_utils as du

def loadmain(request):
    return render(request, "myapp/podcast.html")

def load_podcast(request):
    con, cursor = du.db_connect('postgres')
    cursor.execute("select * from public.podcast")
    podcasts = cursor.fetchall()
    con.close()
    return JsonResponse({'podcasts': podcasts})