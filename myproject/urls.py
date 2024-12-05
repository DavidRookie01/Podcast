from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect root URL (/) to /myapp/podcast/
    path('', lambda request: HttpResponseRedirect('/myapp/podcast/')),  
    
    # Include the URLs from myapp
    path('myapp/podcast/', include('myapp.urls')),  
]
