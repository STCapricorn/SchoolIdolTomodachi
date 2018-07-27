# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.db import models
from django.utils import timezone
from django.conf import settings as django_settings
from magi.utils import PastOnlyValidator, staticImageURL, ordinalNumber
from magi.abstract_models import BaseAccount
from magi.item_model import MagiModel, i_choices, getInfoFromChoices
from magi.models import uploadItem
from sukutomo.django_translated import t

class Account(BaseAccount):
    collection_name = 'account'

    # Foreign keys

    #center = models.ForeignKey('OwnedCard', verbose_name=_('Center'), null=True, help_text=_('The character that talks to you on your home screen.'), on_delete=models.SET_NULL)
    #starter = models.ForeignKey(Card, verbose_name=_('Starter'), null=True, help_text=_('The character that you selected when you started playing.'), on_delete=models.SET_NULL)

    # Details

    VERSIONS = OrderedDict((
        ('JP', { 'translation': _('Japanese version'), 'image': 'ja', 'prefix': 'jp_' }),
        ('WW', { 'translation': _('Worldwide version'), 'image': 'world', 'prefix': 'ww_' }),
        ('KR', { 'translation': _('Korean version'), 'image': 'kr', 'prefix': 'kr_' }),
        ('CN', { 'translation': _('Chinese version'), 'image': 'zh-hans', 'prefix': 'cn_' }),
        ('TW', { 'translation': _('Taiwanese version'), 'image': 'zh-hant', 'prefix': 'tw_' }),
    ))

    VERSION_CHOICES = [(name, info['translation']) for name, info in VERSIONS.items()]
    i_version = models.PositiveIntegerField(_('Version'), choices=i_choices(VERSION_CHOICES), default=1)
    version_image = property(getInfoFromChoices('version', VERSIONS, 'image'))

    friend_id = models.PositiveIntegerField(_('Friend ID'), null=True, help_text=_('You can find your friend id by going to the "Friends" section from the home, then "ID Search". Players will be able to send you friend requests or messages using this number.'))
    show_friend_id = models.BooleanField(_('Should your friend ID be visible to other players?'), default=True)
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests'), null=True)
    device = models.CharField(_('Device'), help_text=_('The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True)
    loveca = models.PositiveIntegerField(_('Love gems'), help_text=string_concat(_('Number of {} you currently have in your account.').format(_('Love gems')), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), null=True)
    friend_points = models.PositiveIntegerField(_('Friend Points'), help_text=string_concat(_('Number of {} you currently have in your account.').format(_('Friend Points')), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), null=True)
    g = models.PositiveIntegerField('G', help_text=string_concat(_('Number of {} you currently have in your account.').format('G'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), null=True)
    tickets = models.PositiveIntegerField('Scouting Tickets', help_text=string_concat(_('Number of {} you currently have in your account.').format('Scouting Tickets'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), null=True)
    vouchers = models.PositiveIntegerField('Vouchers (blue tickets)', help_text=string_concat(_('Number of {} you currently have in your account.').format('Vouchers (blue tickets)'), ' ', _('This field is completely optional, it\'s here to help you manage your accounts.')), null=True)
    bought_loveca = models.PositiveIntegerField(_('Total love gems bought'), help_text=_('You can calculate that number in "Other" then "Purchase History".'), null=True)
    show_items = models.BooleanField('', default=True, help_text=_('Should your items be visible to other players?'))

    # Choices

    PLAY_WITH = OrderedDict([
        ('Thumbs', {
            'translation': _('Thumbs'),
            'icon': 'thumbs'
        }),
        ('Fingers', {
            'translation': _('All fingers'),
            'icon': 'fingers'
        }),
        ('Index', {
            'translation': _('Index fingers'),
            'icon': 'index'
        }),
        ('Hand', {
            'translation': _('One hand'),
            'icon': 'fingers'
        }),
        ('Other', {
            'translation': _('Other'),
            'icon': 'sausage'
        }),
    ])
    PLAY_WITH_CHOICES = [(name, info['translation']) for name, info in PLAY_WITH.items()]

    i_play_with = models.PositiveIntegerField(_('Play with'), choices=i_choices(PLAY_WITH_CHOICES), null=True)

    OS_CHOICES = (
        'Android',
        'iOs',
    )
    i_os = models.PositiveIntegerField(_('Operating System'), choices=i_choices(OS_CHOICES), null=True)

    # Special

    transfer_code = models.CharField('Transfer Code', max_length=100, help_text='It\'s important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.')
    fake = models.BooleanField('Fake', default=False)

    #verified = models.PositiveIntegerField(_('Verified'), default=0, choices=VERIFIED_CHOICES)
    #default_tab = models.CharField(_('Default tab'), max_length=30, choices=ACCOUNT_TAB_CHOICES, help_text=_('What people see first when they take a look at your account.'), default='deck')

    # Cache: leaderboard per version

    def update_cache_leaderboards(self):
        self._cache_leaderboards_last_update = timezone.now()
        self._cache_leaderboard = type(self).objects.filter(
            level__gt=self.level,
            i_version=self.i_version,
        ).values('level').distinct().count() + 1

############################################################
# Idols

LANGUAGES_NEED_OWN_NAME = [ l for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
ALL_ALT_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]

class Idol(MagiModel):
    collection_name = 'idol'

    owner = models.ForeignKey(User, related_name='added_idols')
    name = models.CharField(_('Name'), max_length=100, unique=True)

    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_names = models.TextField(null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'), null=True)

    ATTRIBUTE_CHOICES = (
        ('smile', _('Smile')),
        ('pure', _('Pure')),
        ('cool', _('Cool')),
        ('all', _('All')),
    )

    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=i_choices(ATTRIBUTE_CHOICES), null=True)
    @property
    def attribute_image_url(self): return staticImageURL(self.i_attribute, folder='i_attribute', extension='png')

    UNIT_CHOICES = (
        u'μ\'s',
        'Aqours',
    )

    i_unit = models.PositiveIntegerField(_('Unit'), choices=i_choices(UNIT_CHOICES), null=True)

    SUBUNIT_CHOICES = (
        'Printemps',
        'Lily White',
        'BiBi',
        'CYaRon',
        'AZALEA',
        'Guilty Kiss',
        'Saint Snow',
        'A-RISE',
    )

    i_subunit = models.PositiveIntegerField(_('Subunit'), choices=i_choices(SUBUNIT_CHOICES), null=True)

    SCHOOL_CHOICES = [
        ('chitose', _('Chitose Bridge High School')),
        ('seiran', _('Seiran High School')),
        ('shinonome', _('Shinonome Academy')),
        ('shion', _('Shion Girls\' Academy')),
        ('touou', _('Touou Academy')),
        ('yg', _('Y.G. International Academy')),
        ('nijigasaki', _('Nijigasaki High School')),
        ('uranohoshi', _('Uranohoshi Girls\' High School')),
        ('otonokizaka', _('Otonokizaka Academy')),
    ]

    i_school = models.PositiveIntegerField(_('School'), choices=i_choices(SCHOOL_CHOICES), null=True)

    YEAR_CHOICES = [
        # Needs to be re-translated before being displayed
        ('first', _(u'{nth} year').format(nth=_(ordinalNumber(1)))),
        ('second', _(u'{nth} year').format(nth=_(ordinalNumber(2)))),
        ('third', _(u'{nth} year').format(nth=_(ordinalNumber(3)))),
    ]

    i_year = models.PositiveIntegerField(_('School year'), choices=i_choices(YEAR_CHOICES), null=True)

    age = models.PositiveIntegerField(_('Age'), null=True)
    birthday = models.DateField(_('Birthday'), null=True)

    ASTROLOGICAL_SIGN_CHOICES = (
        ('leo', _('Leo')),
        ('aries', _('Aries')),
        ('libra', _('Libra')),
        ('virgo', _('Virgo')),
        ('scorpio', _('Scorpio')),
        ('capricorn', _('Capricorn')),
        ('pisces', _('Pisces')),
        ('gemini', _('Gemini')),
        ('cancer', _('Cancer')),
        ('sagittarius', _('Sagittarius')),
        ('aquarius', _('Aquarius')),
        ('taurus', _('Taurus')),
    )

    i_astrological_sign = models.PositiveIntegerField(_('Astrological sign'), choices=i_choices(ASTROLOGICAL_SIGN_CHOICES), null=True)
    @property
    def astrological_sign_image_url(self): return staticImageURL(self.i_astrological_sign, folder='i_astrological_sign', extension='png')

    BLOOD_CHOICES = (
        'O',
        'A',
        'B',
        'AB',
    )

    i_blood = models.PositiveIntegerField(_('Blood type'), choices=i_choices(BLOOD_CHOICES), null=True)

    MEASUREMENT_DETAILS = [
        ('height', _('Height')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hips', _('Hips')),
    ]

    height = models.PositiveIntegerField(_('Height'), null=True, default=None)
    bust = models.PositiveIntegerField(_('Bust'), null=True)
    waist = models.PositiveIntegerField(_('Waist'), null=True)
    hips = models.PositiveIntegerField(_('Hips'), null=True)

    hobbies = models.CharField(_('Hobbies'), max_length=100, null=True)

    HOBBIESS_CHOICES = ALL_ALT_LANGUAGES
    d_hobbiess = models.TextField(null=True)

    favorite_food = models.CharField(_('Favorite food'), max_length=100, null=True)

    FAVORITE_FOODS_CHOICES = ALL_ALT_LANGUAGES
    d_favorite_foods = models.TextField(_('Favorite food'), null=True)

    least_favorite_food = models.CharField(_('Least favorite food'), max_length=100, null=True)

    LEAST_FAVORITE_FOODS_CHOICES = ALL_ALT_LANGUAGES
    d_least_favorite_foods = models.TextField(null=True)

    description = models.TextField(_('Description'), null=True)

    DESCRIPTIONS_CHOICES = ALL_ALT_LANGUAGES
    d_descriptions = models.TextField(null=True)

############################################################
# Events

class Event(MagiModel):
    collection_name = 'event'
    owner = models.ForeignKey(User, related_name='added_events')

    title = models.CharField(_('Title'), max_length=100)
    TITLES_CHOICES = ALL_ALT_LANGUAGES
    d_titles = models.TextField(null=True)

    image = models.ImageField(_('Image'), null=True)

    TYPE_CHOICES = (
        ('token', _('Token')),
        ('sm', _('Score Match')),
        ('mf', _('Medley Festival')),
        ('cf', _('Challenge Festival')),
        ('as', _('Adventure Stroll')),
        ('fm', _('Friendly Match')),
    )

    i_type = models.PositiveIntegerField(_('Event type'), choices=i_choices(TYPE_CHOICES), null=True)

    UNIT_CHOICES = (
        u'μ\'s',
        'Aqours',
    )

    i_unit = models.PositiveIntegerField(_('Unit'), choices=i_choices(UNIT_CHOICES), null=True)

    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    jp_image = models.ImageField(string_concat(_('Japanese version'), '-',_('Image')), upload_to=uploadItem('e'), null=True)
    jp_start_date = models.DateTimeField(string_concat(_('Japanese version'), ' - ', _('Beginning')), null=True)
    jp_end_date = models.DateTimeField(string_concat(_('Japanese version'), ' - ',_('End')), null=True)

    ww_image = models.ImageField(string_concat(_('Worldwide version'), '-',_('Image')), upload_to=uploadItem('e'), null=True)
    ww_start_date = models.DateTimeField(string_concat(_('Worldwide version'), ' - ', _('Beginning')), null=True)
    ww_end_date = models.DateTimeField(string_concat(_('Worldwide version'), ' - ',_('End')), null=True)

    tw_image = models.ImageField(string_concat(_('Taiwanese version'), '-', _('Image')), upload_to=uploadItem('e'), null=True)
    tw_start_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ', _('Beginning')), null=True)
    tw_end_date = models.DateTimeField(string_concat(_('Taiwanese version'), ' - ',_('End')), null=True)

    kr_image = models.ImageField(string_concat(_('Korean version'), '-',_('Image')), upload_to=uploadItem('e'), null=True)
    kr_start_date = models.DateTimeField(string_concat(_('Korean version'), ' - ', _('Beginning')), null=True)
    kr_end_date = models.DateTimeField(string_concat(_('Korean version'), ' - ',_('End')), null=True)

    cn_image = models.ImageField(string_concat(_('Chinese version'), '-',_('Image')), upload_to=uploadItem('e'), null=True)
    cn_start_date = models.DateTimeField(string_concat(_('Chinese version'), ' - ', _('Beginning')), null=True)
    cn_end_date = models.DateTimeField(string_concat(_('Chinese version'), ' - ',_('End')), null=True)

    def get_status(self, version='JP'):
        start_date = getattr(self, u'{}start_date'.format(Account.VERSIONS[version]['prefix']))
        end_date = getattr(self, u'{}end_date'.format(Account.VERSIONS[version]['prefix']))
        if not end_date or not start_date:
            return None
        now = timezone.now()
        if now > end_date:
            return 'ended'
        elif now > start_date:
            return 'current'
        return 'future'

    jp_status = property(lambda _s: _s.get_status())
    ww_status = property(lambda _s: _s.get_status(version='WW'))
    tw_status = property(lambda _s: _s.get_status(version='TW'))
    kr_status = property(lambda _s: _s.get_status(version='KR'))
    cn_status = property(lambda _s: _s.get_status(version='CN'))
