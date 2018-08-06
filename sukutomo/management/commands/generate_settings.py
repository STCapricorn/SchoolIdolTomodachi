import datetime, time
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language, activate as translation_activate, ugettext_lazy as _
from django.utils.formats import dateformat
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as django_settings
from magi.tools import totalDonators, getStaffConfigurations, latestDonationMonth
from magi.utils import birthdays_within
from sukutomo import models

def generate_settings():

    print 'Get max stats'
    stats = {
        'smile_max_idol': None,
        'pure_max_idol': None,
        'cool_max_idol': None,
    }
    try:
        for stat in stats.keys():
            max_stats = models.Card.objects.all().extra(select={
            }).order_by('-' + stat)[0]
            stats[stat] = getattr(max_stats, stat)
    except IndexError:
        pass

    print 'Save generated settings'
    s = u'\
# -*- coding: utf-8 -*-\n\
import datetime\n\
MAX_STATS = ' + unicode(stats) + u'\n\
'
    print s
    with open(django_settings.BASE_DIR + '/' + django_settings.SITE + '_project/generated_settings.py', 'w') as f:
        f.write(s.encode('utf8'))
        f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
