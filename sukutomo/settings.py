# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _, string_concat
from magi.utils import tourldash
from magi.default_settings import (
    DEFAULT_LANGUAGES_CANT_SPEAK_ENGLISH,
    DEFAULT_ENABLED_NAVBAR_LISTS,
    DEFAULT_NAVBAR_ORDERING,
    DEFAULT_ENABLED_PAGES,
)
from sukutomo import models

############################################################
# License, game and site settings

SITE_NAME = u'School Idol Tomodachi'

GAME_NAME = string_concat(_('Love Live!'), ' ', _('School Idol Festival'))
GAME_URL = 'https://www.school-fes.klabgames.net/'

COLOR = '#e10b80'

############################################################
# Images

SITE_IMAGE = 'sukutomo.png' # TODO
SITE_LOGO = 'sukutomo.png'
# EMAIL_IMAGE = TODO

############################################################
# Settings per languages

SITE_NAME_PER_LANGUAGE = {
    'ja': u'ラブライブ!スクールアイドル友達',
}
SITE_LOGO_PER_LANGUAGE = {
    'ja': 'logo/sukutomo_ja.png'
}

############################################################
# Contact & Social

CONTACT_EMAIL = 'contact@schoolido.lu'
CONTACT_REDDIT = 'db0company'
CONTACT_FACEBOOK = 'SchoolIdolTomodachi'

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'SchoolIdolAPI')

TWITTER_HANDLE = 'schoolidolu'
HASHTAGS = [u'LoveLive', u'LLSIF', u'ラブライブ', u'スクフェス']

############################################################
# Homepage

HOMEPAGE_RIBBON = True

############################################################
# First steps

############################################################
# Activities

############################################################
# User preferences and profiles

USER_COLORS = [
    ('smile', 'Smile', 'smile', '#e6006f'),
    ('pure', 'Pure', 'pure', '#20ab53'),
    ('cool', 'Cool', 'cool', '#0098eb'),
    ('all', 'All', 'all', '#8f56cc'),
]

FAVORITE_CHARACTER_NAME = _('Idol')
FAVORITE_CHARACTER_TO_URL = lambda link: '/idol/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))

DONATORS_STATUS_CHOICES = [
    ('THANKS', 'Thanks'),
    ('SUPPORTER', _('Idol Supporter')),
    ('LOVER', _('Idol Lover')),
    ('AMBASSADOR', _('Idol Ambassador')),
    ('PRODUCER', _('Idol Producer')),
    ('DEVOTEE', _('Ultimate Idol Devotee')),
]

############################################################
# Technical settings

SITE_URL = 'http://schoolido/lu/'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.schoolido.lu/'

DISQUS_SHORTNAME = 'schoolidol'
GOOGLE_ANALYTICS = 'UA-59453399-4'

ACCOUNT_MODEL = models.Account

############################################################
# From settings or generated_settings

TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', 0) or 2
FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)
BACKGROUNDS = getattr(django_settings, 'BACKGROUNDS', None)
LATEST_NEWS = getattr(django_settings, 'LATEST_NEWS', None)

############################################################
# Customize pages

ENABLED_PAGES = DEFAULT_ENABLED_PAGES.copy()

ENABLED_PAGES['wiki'][0]['enabled'] = True
ENABLED_PAGES['wiki'][1]['enabled'] = True
ENABLED_PAGES['wiki'][0]['navbar_link'] = False

ENABLED_PAGES['map']['navbar_link_list'] = 'community'

ENABLED_PAGES['discord'] = {
    'title': 'Discord',
    'icon': 'chat',
    'navbar_link_list': 'community',
    'redirect': 'TODO',
    'new_tab': True,
    'check_permissions': lambda c: c['request'].LANGUAGE_CODE not in DEFAULT_LANGUAGES_CANT_SPEAK_ENGLISH,
}

ENABLED_PAGES['twitter'] = {
    'title': 'Twitter',
    'icon': 'twitter',
    'navbar_link_list': 'community',
    'redirect': 'https://twitter.com/{}'.format(TWITTER_HANDLE),
    'new_tab': True,
    'check_permissions': lambda c: c['request'].LANGUAGE_CODE not in DEFAULT_LANGUAGES_CANT_SPEAK_ENGLISH,
}

ENABLED_PAGES['skills'] = {
    'title': _('Skills'),
    'staff_required': True,
    'permissions_required': ['manage_main_items'],
    'icon': 'sparkle',
    'navbar_link_list': 'staff',
    'redirect': '/skills',
}

ENABLED_PAGES['sifsong_list'] = {
    'title': _('Songs'),
    'icon': 'song',
    'navbar_link': False,
    #'navbar_link_list': 'games',
    'redirect': '/songs/?i_game=0',
}

# Coming soon pages

COMING_SOON_PAGES = {
    'games': [
        ('sifcard_list', _('Cards'), 'deck'),
        ('sifmore', string_concat(_('Songs'), ', ', _('Backgrounds'), ', ', _('Items'), '...'), ''),
        # ('sifset_list', _('Sets'), 'album'),
        # ('urpairs', _('UR pairs'), 'cards'),
        # ('sifbackground_list', _('Backgrounds'), 'pictures'),
        # ('sifitem_list', _('Items'), 'chest'),

        ('allstarscard_list', _('Cards'), 'deck'),
        ('allstarsevent_list', _('Events'), 'event'),

        ('puchi_list', _('Puchis'), 'chibi'),
        ('puchiguruevent_list', _('Events'), 'event'),

        ('sifaccard_list', _('Cards'), 'deck'),
        ('sifacevent_list', _('Events'), 'event'),

        ('siccard_list', _('School Idol Collection'), 'trading-cards'),
        ('weisscard_list', _('Weiss Schwartz'), 'trading-cards'),

        ('schoolidolcontest', _('School Idol Contest'), 'contest'),
        ('schoolidoltrivia', _('School Idol Trivia'), 'star'),
        ('schoolidolmemory', _('School Idol Memory'), 'chat'),
    ],
    'lovelive': [
        ('voiceactress_list', _('Voice actresses'), 'voice-actress'),
        ('episode_list', _('Episodes'), 'play'),
        ('song_list', _('Songs'), 'song'),
    ],
    'shop': [
        ('shop_official', _('Official merchandise'), 'star'),
        ('shop_fan', _('Fan-made items'), 'heart'),
        ('shop_commissions', _('Commissions'), 'author'),
    ],
    'community': [
        ('cosplays', _('Cosplays'), 'dress'),
        ('fanarts', _('Fanarts'), 'edit'),
        ('fanedits', _('Fan edits'), 'pictures'),
        ('fanfictions', _('Fan fictions'), 'author'),
        ('communityevent_list', _('Community events'), 'event'),
    ],
}

for _navbar_link_list, _pages in COMING_SOON_PAGES.items():
    break
    for _page, _title, _icon in _pages:
        ENABLED_PAGES[_page] = {
            'title': _title,
            'redirect': '/comingsoon/?page={}'.format(_page),
            'icon': _icon,
            'navbar_link_list': _navbar_link_list,
        }

ENABLED_PAGES['twitter']['divider_after'] = True
ENABLED_PAGES['discord']['divider_before'] = True

############################################################
# Customize nav bar

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS.copy()

ENABLED_NAVBAR_LISTS['lovelive'] = {
    'title': _('Love Live!'),
    'icon': 'idolized',
    'ordering': [
        'idol_list',
        'voiceactress_list',
        'episode_list',
        'song_list',
    ],
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
    'order': ['account_list', 'map', 'twitter'],
}

NAVBAR_ORDERING = ['lovelive', 'schoolidolfestival', 'community', 'you', 'staff', 'more']

ENABLED_NAVBAR_LISTS['games'] = {
    'icon': 'hobbies',
    'title': _('Games'),
    'headers': [
        ('schoolidolfestival', {
            'image': 'schoolidolfestival',
            'title': _('School Idol Festival'),
        }),
        # ('allstars', {
        #     'image': 'allstars',
        #     'title': _('All Stars'),
        # }),
        # ('puchiguru', {
        #     'image': 'puchiguru',
        #     'title': _('Puchiguru'),
        # }),
        # ('afterschoolactivity', {
        #     'image': 'afterschoolactivity',
        #     'title': _('~After School Activity~'),
        # }),
        # ('tradingcards', {
        #     'icon': 'trading-cards',
        #     'title': _('Trading cards'),
        # }),
        # ('onlineminigames', {
        #     'icon': 'hobbies',
        #     'title': _('Online mini games'),
        # }),
    ],
    'order': [
        'schoolidolfestival',
        'sifcard_list',
        'sifset_list',
        'urpairs',
        'sifevent_list',
        'sifsong_list',
        'sifbackground_list',
        'sifitem_list',
        'sifmore',

        'allstars',
        'allstarscard_list',
        'allstarsevent_list',

        'puchiguru',
        'puchi_list',
        'puchiguruevent_list',

        'afterschoolactivity',
        'sifaccard_list',
        'sifacevent_list',

        'tradingcards',
        'siccard_list',
        'weisscard_list',


        'onlineminigames',
        'schoolidolcontest',
        'schoolidoltrivia',
        'schoolidolmemory',
    ],
}

ENABLED_NAVBAR_LISTS['community'] = {
    'title': _('Community'),
    'icon': 'users',
    'order': [
        'account_list',
        'discord',
        'twitter',

        'communityevent_list',
        'cosplays',
        'fanarts',
        'fanedits',
        'fanfictions',
    ],
}

ENABLED_NAVBAR_LISTS['shop'] = {
    'title': _('Shop'),
    'icon': 'shop',
    'order': [
    ],
}

NAVBAR_ORDERING = [
    'lovelive',
    'games',
    'shop',
    'community',
] + DEFAULT_NAVBAR_ORDERING
