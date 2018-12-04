import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as django_settings
from django.utils import timezone
from django.db.models import Q
from magi.tools import (
    totalDonatorsThisMonth,
    latestDonationMonth,
    getStaffConfigurations,
    generateSettings,
)
from sukutomo import models
from sukutomo.utils import sortIdolUnit

def generate_settings():

    now = timezone.now()
    two_days_ago = now - datetime.timedelta(days=2)

    print 'Get total donators'
    total_donators = totalDonatorsThisMonth() or '\'\''

    print 'Get latest donation month'
    donation_month = latestDonationMonth(failsafe=True)

    print 'Get staff configurations and latest news'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Add events to latest news'
    events_condition = Q()
    for version, version_details in [
            (k, v) for k, v in models.VERSIONS
            if k in models.IMPORTANT_VERSIONS
    ]:
        events_condition |= Q(**{ '{}end_date__gte': two_days_ago })
    recent_events = models.SIFEvent.objects.filter(events_condition)
    latest_news += [{
        'title': event.name,
        'image': event.image_url,
        'url': event.item_url,
    } for event in recent_events]

    print 'Get the characters'
    all_idols = sortIdolUnit(models.Idol.objects.all())
    favorite_characters = [(
        idol.pk,
        idol.name,
        idol.image_url,
    ) for idol in all_idols]

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

    generateSettings({
        'LATEST_NEWS': latest_news,
        'TOTAL_DONATORS': total_donators,
        'DONATION_MONTH': donation_month,
        'STAFF_CONFIGURATIONS': staff_configurations,
        'FAVORITE_CHARACTERS': favorite_characters,
        'MAX_STATS': stats,
        # 'BACKGROUNDS': backgrounds,
    })

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
