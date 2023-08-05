from django.conf.urls import url
from django.contrib import admin
from django_portmaster.urls import portmaster_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls)
]

urlpatterns += portmaster_urlpatterns
