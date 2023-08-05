from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django_portmaster.models import Service
from django_portmaster.models import Offer
from django_portmaster.models import Instance
from django_portmaster.serializers import ServiceSerializer
from django_portmaster.serializers import OfferSerializer
from django_portmaster.serializers import InstanceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer
    lookup_field = 'name'


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('service', 'port')
    serializer_class = OfferSerializer
    lookup_field = 'secret'

    def list(self, request, service_name):
        offers = self.queryset.filter(service=service_name)
        if offers:
            serializer = self.get_serializer(offers, many=True)
            return Response(serializer.data)

        return Response([])

    def create(self, request, service_name):
        service = get_object_or_404(Service, name=service_name)
        request.data['port'] = service.next()
        request.data['service'] = service.name
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, service_name, secret):
        return Response({'detail': "Method 'PUT' not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, service_name, secret):
        return Response({'detail': "Method 'PATCH' not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @detail_route(methods=['post'])
    def accept(self, request, service_name, secret):
        offer = get_object_or_404(Offer, secret=secret)

        if offer.service.instance_set.filter(name=offer.name):
            raise serializers.ValidationError('Service instance with this name '
                                              'already exists.')

        instance = offer.accept()
        serializer = InstanceSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @detail_route(methods=['post'])
    def reject(self, request, service_name, secret):
        offer = get_object_or_404(Offer, secret=secret)
        offer.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)


class InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.all().order_by('port')
    serializer_class = InstanceSerializer

    def get_object(self):
        queryset = self.get_queryset()

        if self.kwargs['pk'].isdecimal():
            obj = get_object_or_404(queryset, port=self.kwargs['pk'])
        else:
            obj = get_object_or_404(queryset, name=self.kwargs['pk'])

        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, service_name):
        return Response({'detail': "Method 'POST' not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, service_name, pk):
        return Response({'detail': "Method 'PUT' not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, service_name, pk):
        return Response({'detail': "Method 'PATCH' not allowed."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
