from django.urls import path, include

urlpatterns = [
    path('planning/', include('planning.urls')),
]

