from django.conf.urls import url
from django.conf.urls import include
from rest_framework_nested import routers
from django_portmaster import api_v1 as service_api_v1

portmaster_v1 = routers.SimpleRouter(trailing_slash=False)
portmaster_v1.register('services', service_api_v1.ServiceViewSet)

nested_api_v1 = routers.NestedSimpleRouter(portmaster_v1,
                                           r'services',
                                           trailing_slash=False,
                                           lookup='service')
nested_api_v1.register(r'offers',
                       service_api_v1.OfferViewSet,
                       base_name='service-offer')

nested_api_v1.register(r'ports',
                       service_api_v1.InstanceViewSet,
                       base_name='service-instance')


portmaster_urlpatterns = [
    url(r'^v1/', include(portmaster_v1.urls)),
    url(r'^v1/', include(nested_api_v1.urls)),
]
