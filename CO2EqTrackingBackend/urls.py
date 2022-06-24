from django.contrib import admin
from django.urls import path, include


#################################################### END-OF-IMPORT #################################################


urlpatterns = [
    path('auth/', include('account.urls')),
    path('record/', include('record.urls')),
    path('admin/', admin.site.urls)
]
