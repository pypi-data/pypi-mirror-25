import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django_portmaster.common import delete_offers_after_minutes


class Service(models.Model):
    """This is where we define a simple service. Besides
    name, service has only two required properties:

    start: where does the port range start
    end: where does the port range end
    """
    name = models.CharField('name', max_length=64, primary_key=True)
    description = models.TextField('description',
                                   null=True, blank=True, default=None)
    start = models.IntegerField('start')
    end = models.IntegerField('end')

    @property
    def range(self):
        return list(range(self.start, self.end + 1))

    def available(self):
        used = [i.port for i in self.instance_set.all()]
        used += [i.port for i in self.offer_set.all()]
        used = set(self.range).difference(used)
        return list(used)

    def next(self):
        available = self.available()
        return available[0] if available else -1


class OfferManager(models.Manager):
    def cleanup_offers(self):
        offset = timezone.now() - timedelta(minutes=delete_offers_after_minutes)
        Offer.objects.filter(created__lte=offset).delete()


class Offer(models.Model):
    service = models.ForeignKey('Service')
    port = models.IntegerField('port', unique=True)
    name = models.CharField('name', max_length=64)
    secret = models.UUIDField('secret', primary_key=True, default=uuid.uuid4,
                              editable=False)
    created = models.DateTimeField('created', auto_now=False, auto_now_add=True)

    objects = OfferManager()

    class Meta:
        unique_together = ('service', 'name')

    def accept(self):
        instance = Instance.objects.create(
            service=self.service,
            port=self.port,
            name=self.name
        )
        self.delete()

        return instance


class Instance(models.Model):
    """When a Service is created port entries
    will be automatically created as Instances.

    When port is allocated, a service instance name
    will be added to it.
    """
    service = models.ForeignKey('Service')
    port = models.IntegerField('port', primary_key=True)
    name = models.CharField('name', max_length=64,
                            null=True, blank=True, default=None)
    created = models.DateTimeField('created', auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = ('service', 'name')
