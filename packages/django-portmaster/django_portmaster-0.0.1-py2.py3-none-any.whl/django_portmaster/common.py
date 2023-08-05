from django.conf import settings

if hasattr(settings, 'PM_DELETE_OFFERS_AFTER_MINUTES'):
    delete_offers_after_minutes = settings.PM_DELETE_OFFERS_AFTER_MINUTES
else:
    delete_offers_after_minutes = 30
