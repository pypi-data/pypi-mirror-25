from django.db.models import Q
from rest_framework import serializers
from django_portmaster.models import Service
from django_portmaster.models import Offer
from django_portmaster.models import Instance


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'description', 'start', 'end')

    def __validate_port_range(self, value):
        """Port range should not be in reserved ranges
        """
        if value < 1024 or value >= 49152:
            raise serializers.ValidationError('Port range is in reserved range.')

        return value

    def __validate_start_stop(self, data):
        """Start of the range should be a lower number
        """
        if data['start'] >= data['end']:
            raise serializers.ValidationError('Start of the range should be a '
                                              'lower number.')

        return data

    def __validate_overlap(self, data):
        """Make sure that the port ranges do not overlap
        """
        services = Service.objects.filter(
            Q(start__lte=data['start'], end__gte=data['start']) |
            Q(start__lte=data['end'], end__gte=data['end']) |
            Q(start__gte=data['start'], end__lte=data['end'])
        ).exclude(name=data['name'])

        if services:
            raise serializers.ValidationError('Port range overlaps with '
                                              'existing services.')

        return data

    def __validate_update(self, data):
        """Make sure that existing service instances do not
        fall outside of the range
        """
        services = Instance.objects.filter(
            Q(port__lt=data['start']) | Q(port__gt=data['end']),
            service__name=data['name']
        )

        if services:
            raise serializers.ValidationError('Defined service instances '
                                              'fall outside of the range.')

        return data

    def validate_start(self, value):
        return self.__validate_port_range(value)

    def validate_end(self, value):
        return self.__validate_port_range(value)

    def validate(self, data):
        self.__validate_start_stop(data)
        self.__validate_overlap(data)
        self.__validate_update(data)

        return data


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('service', 'name', 'port', 'secret', 'created')

    def validate_port(self, value):
        if value == -1:
            raise serializers.ValidationError('Port range has been completely '
                                              'utilized.')

        return value


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ('service', 'name', 'port', 'created')
