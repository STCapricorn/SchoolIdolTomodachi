# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from sukutomo import models
from magi.utils import tourldash
from magi.default_settings import DEFAULT_ENABLED_NAVBAR_LISTS, DEFAULT_ENABLED_PAGES

SITE_NAME = 'LoveLive! School Idol Tomodachi'
SITE_URL = 'http://schoolido/lu/'
SITE_IMAGE = 'sukutomo.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.schoolido.lu/'
GAME_NAME = 'LoveLive! School Idol Festival'
DISQUS_SHORTNAME = 'schoolidol'
ACCOUNT_MODEL = models.Account
COLOR = '#e10b80'

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'SchoolIdolAPI')
CONTACT_EMAIL = 'contact@schoolido.lu'

DONATORS_STATUS_CHOICES = [
    ('THANKS', 'Thanks'),
    ('SUPPORTER', _('Idol Supporter')),
    ('LOVER', _('Idol Lover')),
    ('AMBASSADOR', _('Idol Ambassador')),
    ('PRODUCER', _('Idol Producer')),
    ('DEVOTEE', _('Ultimate Idol Devotee')),
#    ('STAFF', _('Staff')),
#    ('DATABASE', _('Database Maintainer')),
]

GAME_URL = 'https://www.school-fes.klabgames.net/'

GOOGLE_ANALYTICS = 'UA-59453399-4'
HASHTAGS = ['LoveLive', 'LLSIF', 'ラブライブ', 'スクフェス']

TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', 2) + 2

TWITTER_HANDLE = 'schoolidolu'

USER_COLORS = [
    ('smile', 'Smile', 'btn-smile', '#e6006f'),
    ('pure', 'Pure', 'btn-pure', '#20ab53'),
    ('cool', 'Cool', 'btn-cool', '#0098eb'),
    ('all', 'All', 'btn-all', '#8f56cc'),
]

# todo
# SITE_LOGO = Path of the image displayed on the homepage.	value of SITE_IMAGE
# FAVORITE_CHARACTERS = django_settings.FAVORITE_CHARACTERS
FAVORITE_CHARACTER_NAME = _('{nth} Favorite Character')
FAVORITE_CHARACTER_TO_URL = lambda link: '/idol/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
# LATEST_NEWS = django_settings.LATEST_NEWS
# ABOUT_PHOTO
# ACTIVITY_TAGS
# EMAIL_IMAGE
# ENABLED_PAGES: ur pairs

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['wiki'][0]['enabled'] = True
ENABLED_PAGES['wiki'][1]['enabled'] = True
ENABLED_PAGES['wiki'][0]['divider_before'] = True
ENABLED_PAGES['wiki'][0]['navbar_link_list'] = 'schoolidolfestival'

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS
ENABLED_NAVBAR_LISTS['lovelive'] = {
    'title': _('LoveLive!'),
    'icon': 'heart',
    'order': ['idol_list', 'song_list'],
}
ENABLED_NAVBAR_LISTS['schoolidolfestival'] = {
    'title': _('School Idol Festival'),
    'icon': 'music',
    'order': [
        'card_list', 'set_list', 'event_list',
        'wiki',
    ],
}
ENABLED_NAVBAR_LISTS['community'] = {
    'title': _('Community'),
    'icon': 'users',
    'order': ['activity_list', 'account_list', 'map', 'donate_list', 'twitter'],
}
