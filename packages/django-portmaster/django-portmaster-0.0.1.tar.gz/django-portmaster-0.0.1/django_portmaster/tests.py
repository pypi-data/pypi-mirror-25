from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase

from django_portmaster.common import delete_offers_after_minutes
from django_portmaster.models import Service
from django_portmaster.models import Offer
from django_portmaster.models import Instance


class ServiceApiTests(APITestCase):
    fixtures = ['service_testdata.json',
                'offer_testdata.json',
                'instance_testdata.json']

    def test_service_list(self):
        url = reverse('service-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        django = response.data[0]
        self.assertEqual(django['name'], 'Django')
        self.assertEqual(django['description'], 'Django service')
        self.assertEqual(django['start'], 5000)
        self.assertEqual(django['end'], 10000)

    def test_service_create(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 15001,
                'end': 20000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 3)

        service = Service.objects.get(name='CherryPy')
        self.assertEqual(service.description, 'CherryPy service')
        self.assertEqual(service.start, 15001)
        self.assertEqual(service.end, 20000)

    def test_service_create_privilege_ports(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 1000,
                'end': 2000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_create_iana_ephemeral_ports(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 40000,
                'end': 50000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_create_start_overlap(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 12000,
                'end': 20000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_create_end_overlap(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 2000,
                'end': 8000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_create_total_overlap(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 2000,
                'end': 20000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_create_start_end_mismatch(self):
        url = reverse('service-list')
        data = {'name': 'CherryPy',
                'description': 'CherryPy service',
                'start': 3000,
                'end': 2000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_create_duplicated_name(self):
        url = reverse('service-list')
        data = {'name': 'Django',
                'description': 'Django service',
                'start': 15000,
                'end': 20000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Service.objects.count(), 2)

    def test_service_update(self):
        url = reverse('service-detail', kwargs={'name': 'Django'})
        data = {'name': 'Django',
                'description': 'Django service test',
                'start': 4000,
                'end': 9000}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        service = Service.objects.get(name='Django')
        self.assertEqual(service.description, 'Django service test')
        self.assertEqual(service.start, 4000)
        self.assertEqual(service.end, 9000)

    def test_service_update_out_of_range(self):
        url = reverse('service-detail', kwargs={'name': 'Django'})
        data = {'name': 'Django',
                'description': 'Django service',
                'start': 6000,
                'end': 10000}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        service = Service.objects.get(name='Django')
        self.assertEqual(service.start, 5000)

    def test_service_port_range(self):
        service = Service.objects.get(name='Django')
        self.assertEqual(len(service.range), 5001)
        self.assertEqual(service.range[0], 5000)
        self.assertEqual(service.range[-1], 10000)

    def test_service_available_ports(self):
        service = Service.objects.get(name='Django')
        available = service.available()
        self.assertEqual(len(available), 4999)
        self.assertEqual(available[0], 5002)
        self.assertEqual(available[-1], 10000)

        service.instance_set.first().delete()
        available = service.available()
        self.assertEqual(len(available), 5000)
        self.assertEqual(available[0], 5000)
        self.assertEqual(available[-1], 10000)

    def test_service_next_port(self):
        service = Service.objects.get(name='Django')
        self.assertEqual(service.next(), 5002)

        service.instance_set.first().delete()
        self.assertEqual(service.next(), 5000)


class OfferApiTests(APITestCase):
    fixtures = ['service_testdata.json',
                'offer_testdata.json',
                'instance_testdata.json']

    def setUp(self):
        super(OfferApiTests, self).setUp()

        offer = Offer.objects.all().first()
        offer.created = timezone.now() - timedelta(minutes=5)
        offer.save()
        self.offer_created = offer.created

    def test_offer_list(self):
        url = reverse('service-offer-list', kwargs={'service_name': 'Django'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        web_02 = response.data[0]
        self.assertEqual(web_02['service'], 'Django')
        self.assertEqual(web_02['name'], 'Web-02')
        self.assertEqual(web_02['port'], 5001)
        self.assertEqual(web_02['secret'], 'aafae2f7-4bdb-493c-beea-48bebe51f125')

    def test_offer_create(self):
        url = reverse('service-offer-list', kwargs={'service_name': 'Django'})
        data = {'name': 'Web-03'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)

        offer = Offer.objects.get(name='Web-03')
        self.assertEqual(offer.service.name, 'Django')
        self.assertEqual(offer.port, 5002)

    def test_offer_create_duplicated_name(self):
        url = reverse('service-offer-list', kwargs={'service_name': 'Django'})
        data = {'name': 'Web-02'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Offer.objects.count(), 1)

    def test_offer_create_out_of_ports(self):
        url = reverse('service-detail', kwargs={'name': 'Django'})
        data = {'name': 'Django',
                'description': 'Django service test',
                'start': 5000,
                'end': 5001}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('service-offer-list', kwargs={'service_name': 'Django'})
        data = {'name': 'Web-02'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(response.data['port'], ['Port range has been completely utilized.'])

    def test_offer_update_put(self):
        url = reverse('service-offer-detail',
                      kwargs={'service_name': 'Django',
                              'secret': 'aafae2f7-4bdb-493c-beea-48bebe51f125'})
        data = {'name': 'Web-03'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_offer_update_patch(self):
        url = reverse('service-offer-detail',
                      kwargs={'service_name': 'Django',
                              'secret': 'aafae2f7-4bdb-493c-beea-48bebe51f125'})
        data = {'name': 'Web-03'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_offer_clean_old_offers(self):
        offer = Offer.objects.all().first()
        offer.created = timezone.now() - timedelta(minutes=delete_offers_after_minutes + 5)
        offer.save()

        url = reverse('service-offer-list', kwargs={'service_name': 'Django'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_offer_accept(self):
        url = reverse(
            'service-offer-accept',
            kwargs={'service_name': 'Django',
                    'secret': 'aafae2f7-4bdb-493c-beea-48bebe51f125'}
        )
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        offers = Offer.objects.filter(secret='aafae2f7-4bdb-493c-beea-48bebe51f125')
        self.assertEqual(offers.count(), 0)

        instances = Instance.objects.filter(name='Web-02',
                                            service='Django',
                                            port=5001)
        self.assertEqual(instances.count(), 1)

    def test_offer_accept_duplicate_name(self):
        offer = Offer.objects.all().first()
        offer.name = 'Web-01'
        offer.save()

        url = reverse(
            'service-offer-accept',
            kwargs={'service_name': 'Django',
                    'secret': 'aafae2f7-4bdb-493c-beea-48bebe51f125'}
        )
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        offers = Offer.objects.filter(secret='aafae2f7-4bdb-493c-beea-48bebe51f125')
        self.assertEqual(offers.count(), 1)

    def test_offer_reject(self):
        url = reverse(
            'service-offer-reject',
            kwargs={'service_name': 'Django',
                    'secret': 'aafae2f7-4bdb-493c-beea-48bebe51f125'}
        )
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        offers = Offer.objects.filter(secret='aafae2f7-4bdb-493c-beea-48bebe51f125')
        self.assertEqual(offers.count(), 0)

        instances = Instance.objects.filter(name='Web-02',
                                            service='Django',
                                            port=5001)
        self.assertEqual(instances.count(), 0)


class InstanceApiTests(APITestCase):
    fixtures = ['service_testdata.json', 'instance_testdata.json']

    def test_instance_list(self):
        url = reverse('service-instance-list', kwargs={'service_name': 'Django'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        web_01 = response.data[0]
        self.assertEqual(web_01['service'], 'Django')
        self.assertEqual(web_01['name'], 'Web-01')
        self.assertEqual(web_01['port'], 5000)

    def test_instance_detail_by_port(self):
        url = reverse('service-instance-detail',
                      kwargs={'service_name': 'Django', 'pk': 5000})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['service'], 'Django')
        self.assertEqual(response.data['name'], 'Web-01')
        self.assertEqual(response.data['port'], 5000)

    def test_instance_detail_by_name(self):
        url = reverse('service-instance-detail',
                      kwargs={'service_name': 'Django', 'pk': 'Web-01'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['service'], 'Django')
        self.assertEqual(response.data['name'], 'Web-01')
        self.assertEqual(response.data['port'], 5000)

    def test_instance_create(self):
        url = reverse('service-instance-list', kwargs={'service_name': 'Django'})

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_instance_update_put(self):
        url = reverse('service-instance-detail',
                      kwargs={'service_name': 'Django', 'pk': 'Web-01'})
        data = {'name': 'Web-03'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_instance_update_patch(self):
        url = reverse('service-instance-detail',
                      kwargs={'service_name': 'Django', 'pk': 'Web-01'})
        data = {'name': 'Web-03'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
