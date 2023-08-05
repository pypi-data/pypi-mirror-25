from django_portmaster.models import Offer


class CleanOldOffersMiddleware(object):
    """Clean up offers offers older than PM_DELETE_OFFERS_AFTER_MINUTES.
    Value of PM_DELETE_OFFERS_AFTER_MINUTES defaults to 30 minutes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.cleanup_offers()
        response = self.get_response(request)
        return response

    def cleanup_offers(self):
        Offer.objects.cleanup_offers()
