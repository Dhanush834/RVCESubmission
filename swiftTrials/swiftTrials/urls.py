# mydjangoapp/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('home.urls')),  # Include your app's URLs under 'api/'
]
