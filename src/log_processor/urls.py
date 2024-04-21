from django.contrib import admin
from django.urls import include, path

api_v1 = [
    path('logs/', include('log_processor.logs.api.v1.urls'))
]

api_versioned = [
    path('v1/', include(api_v1))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_versioned))
]
