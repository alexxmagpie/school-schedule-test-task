from django.urls import path, include


urlpatterns = [
    path('api/', include('apps.course.api.urls'))
]
