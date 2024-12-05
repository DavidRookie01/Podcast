from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect root URL (/) to /myapp/podcast/
    path('', lambda request: HttpResponseRedirect('/myapp/podcast/')),  
    
    # Include the URLs from myapp
    path('myapp/podcast/', include('myapp.urls')),  
]

static_urlpatterns = [
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
