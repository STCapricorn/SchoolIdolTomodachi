import datetime, time
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language, activate as translation_activate, ugettext_lazy as _
from django.utils.formats import dateformat
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as django_settings
from magi.tools import generateSettings, totalDonators, getStaffConfigurations, latestDonationMonth
from magi.utils import birthdays_within
from sukutomo import models

def generate_settings():

    print 'Get Staff Configurations'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Get Idols'
    favorite_idols = [(
        idol.pk,
        idol.name,
        idol.image_url,
    ) for idol in models.Idol.objects.all().order_by('-i_school')]

    print 'Save generated settings'
    generateSettings({
        'STAFF_CONFIGURATIONS': staff_configurations,
        'FAVORITE_CHARACTERS': favorite_idols,
    })

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
