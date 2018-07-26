# -*- coding: utf-8 -*-
import datetime, time
from collections import OrderedDict
from django.core.validators import MaxValueValidator, MinValueValidator
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

    VERSION_CHOICES = [(_name, _info['translation']) for _name, _info in VERSIONS.items()]
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
        'android',
        'ios',
    )
    i_os = models.PositiveIntegerField(_('Operating System'), choices=i_choices(OS_CHOICES), null=True)

    # Special

    transfer_code = models.CharField(_('Transfer Code'), max_length=100, help_text=_('It\'s important to always have an active transfer code, since it will allow you to retrieve your account in case you loose your device. We can store it for you here: only you will be able to see it. To generate it, go to the settings and use the first button below the one to change your name in the first tab.'))
    fake = models.BooleanField(_('Fake'), default=False)

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

    def __unicode__(self):
        return self.t_name

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
        ('hakodate', _('Hakodate Seisen Girls\' Academy')),
        ('utx', _('UTX High School')),
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
# Songs

class Song(MagiModel):
    collection_name = 'song'
    owner = models.ForeignKey(User, related_name='added_songs', null=True)

    DIFFICULTY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(12),
    ]

    DIFFICULTIES = (
        ('easy', 'EASY'),
        ('normal', 'NORMAL'),
        ('hard', 'HARD'),
        ('expert', 'EXPERT'),
        ('master', 'MASTER'),
    )

    SONGWRITERS_DETAILS = [
        ('composer', _('Composer')),
        ('lyricist', _('Lyricist')),
        ('arranger', _('Arranger')),
    ]

    title = models.CharField(_('Title'), max_length=100)
    TITLES_CHOICES = ALL_ALT_LANGUAGES
    d_titles = models.TextField(null=True)

    def __unicode__(self):
        return self.t_title

    romaji = models.CharField(string_concat(_('Title'), ' (', _('Romaji'), ')'), max_length=100, null=True)
    cover = models.ImageField(_('Song Cover'), upload_to=uploadItem('s'), null=True)

    ATTRIBUTE_CHOICES = (
        ('smile', _('Smile')),
        ('pure', _('Pure')),
        ('cool', _('Cool')),
    )
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=i_choices(ATTRIBUTE_CHOICES), null=True)

    UNIT_CHOICES = Idol.UNIT_CHOICES
    i_unit = models.PositiveIntegerField(_('Unit'), choices=i_choices(UNIT_CHOICES), null=True)
    
    SUBUNIT_CHOICES = Idol.SUBUNIT_CHOICES
    i_subunit = models.PositiveIntegerField(_('Subunit'), choices=i_choices(SUBUNIT_CHOICES), null=True)

    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    LOCATIONS_CHOICES = [
        ('hits', _('Hits')),
        ('daily', _('Daily rotation')),
        ('bside', _('B-Side')),
    ]
    c_locations = models.TextField(_('Locations'), blank=True, null=True)

    unlock = models.PositiveIntegerField(_('Unlock'), help_text=_('Will be displayed as "Rank __"'), null=True)
    daily = models.CharField(_('Daily rotation'), max_length = 100, null=True)
    b_side_master = models.BooleanField(_('MASTER'), default=False)
    b_side_start = models.DateTimeField(string_concat(_('B-Side'), ' - ', _('Beginning')), null=True)
    b_side_end = models.DateTimeField(string_concat(_('B-Side'), ' - ', _('End')), null=True)

    release = models.DateTimeField(_('Release date'), null=True)  
    itunes_id = models.PositiveIntegerField(_('Preview'), help_text='iTunes ID', null=True)
    length = models.PositiveIntegerField(_('Length'), help_text=_('in seconds'), null=True)
    bpm = models.PositiveIntegerField(_('Beats per minute'), null=True)

    @property
    def length_in_minutes(self):
        return time.strftime('%M:%S', time.gmtime(self.length))

    SONGWRITERS = (
        ('composer', _('Composer')),
        ('lyricist', _('Lyricist')),
        ('arranger', _('Arranger')),
    )

    composer = models.CharField(_('Composer'), max_length=100, null=True)
    lyricist = models.CharField(_('Lyricist'), max_length=100, null=True)
    arranger = models.CharField(_('Arranger'), max_length=100, null=True)

    easy_notes = models.PositiveIntegerField(string_concat('EASY', ' - ', _('Notes')), null=True)
    easy_difficulty = models.PositiveIntegerField(string_concat('EASY', ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    normal_notes = models.PositiveIntegerField(string_concat('NORMAL', ' - ', _('Notes')), null=True)
    normal_difficulty = models.PositiveIntegerField(string_concat('NORMAL', ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    hard_notes = models.PositiveIntegerField(string_concat('HARD', ' - ', _('Notes')), null=True)
    hard_difficulty = models.PositiveIntegerField(string_concat('HARD', ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    expert_notes = models.PositiveIntegerField(string_concat('EXPERT', ' - ', _('Notes')), null=True)
    expert_difficulty = models.PositiveIntegerField(string_concat('EXPERT', ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    master_notes = models.PositiveIntegerField(string_concat('MASTER', ' - ', _('Notes')), null=True)
    master_difficulty = models.PositiveIntegerField(string_concat('MASTER', ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    master_swipe = models.BooleanField(_('with SWIPE notes'), default=False)

    @property
    def status(self):
        start_date = getattr(self, 'b_side_start')
        end_date = getattr(self, 'b_side_end')
        if not end_date or not start_date:
            return None
        now = timezone.now()
        if now > end_date:
            return 'ended'
        elif now > start_date:
            return 'current'
        return 'future'            

    @property
    def available(self):
        release_date = getattr(self, 'release')
        b_side = getattr(self, 'status')
        if b_side is 'current':
            return True
        elif release_date:
            if timezone.now() >= release_date:
                return True
        return False

############################################################
# Skills

class Skill(MagiModel):
    collection_name = 'skill'
    owner = models.ForeignKey(User, related_name='added_skills', null=True)

    def __unicode__(self):
        return u'{}'.format(self.t_name)

    def card_html(self):
        return string_concat('<b>', self.t_name, ' <span class="text-muted">(', self.skill_type, ')</span></b>')

    name = models.CharField(_('Name'), max_length=100, unique=True)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(null=True)

    SKILL_TYPE = (
        ('score', _('Score Up')),
        ('pl', _('Timing Boost')),
        ('heal', _('Recovery')),
        ('stat', _('Stat Effect')),
        ('support', _('Support')),
    )
    i_skill_type =  models.PositiveIntegerField(_('Skill Type'), choices=i_choices(SKILL_TYPE), null=True)

    details = models.TextField(_('Details'), help_text=_('Optional variables: {rate}, {dependency}, {chance}, {unit}, {subunit}, {year}, {number}, {length}'), null=True)
    DETAILS_CHOICES = ALL_ALT_LANGUAGES
    d_detailss = models.TextField(null=True)

############################################################
# Sets

class Set(MagiModel):
    collection_name = 'set'
    owner = models.ForeignKey(User, related_name='added_sets', null=True)

    def __unicode__(self):
        if self.set_type:
            set_type = self.set_type
        else:
            set_type = '???'
        if self.unit_type:
            unit_type = self.unit_type
        else:
            unit_type = '???'   
        return u'{} ({}, {})'.format(self.t_title, set_type, unit_type)

    @property
    def cards_url(self):
        return u'/cards/?in_set={}'.format(self.id)

    @property
    def ajax_cards_url(self):
        return u'/ajax/cards/?in_set={}'.format(self.id)

    title = models.CharField(_('Title'), max_length=100, unique=True)
    TITLES_CHOICES = ALL_ALT_LANGUAGES
    d_titles = models.TextField(null=True)

    SET_TYPES = (
        ('gacha', _('Gacha')),
        ('event', _('Event')),
    )
    i_set_type =  models.PositiveIntegerField(_('Type'), choices=i_choices(SET_TYPES), null=True)

    UNIT_TYPES = Idol.UNIT_CHOICES
    i_unit_type = models.PositiveIntegerField(_('Unit'), choices=i_choices(UNIT_TYPES), null=True)

############################################################
# Cards

class Card(MagiModel):
    collection_name = 'card'
    owner = models.ForeignKey(User, related_name='added_cards', null=True)

    def __unicode__(self):
        rarity = ''
        idol = ''
        attribute = ''
        if self.rarity:
            rarity=self.rarity
        if self.idol:
            idol=self.idol
        if self.attribute:
            attribute = self.t_attribute
        return u'#{} {} {} {}'.format(self.card_id, attribute, rarity, idol)

    card_id = models.PositiveIntegerField(_('ID'), unique=True)
    idol = models.ForeignKey(Idol, related_name='card_idols', null=True)

    RARITY_CHOICES = (
        'N',
        'R',
        'SR',
        'SSR',
        'UR',
    )
    i_rarity =  models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES), null=True)

    limited = models.BooleanField(_('Limited'), default=False)
    promo = models.BooleanField(_('Promo'), default=False)
    support = models.BooleanField(_('Support'), default=False)
    
    ATTRIBUTE_CHOICES = Idol.ATTRIBUTE_CHOICES
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=i_choices(ATTRIBUTE_CHOICES), null=True)

    VERSIONS_CHOICES = Account.VERSION_CHOICES
    c_versions = models.TextField(_('Server availability'), blank=True, null=True, default='"JP"')

    release = models.DateTimeField(_('Release date'), null=True)

    name = models.CharField(_('Name'), max_length=100, null=True)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(null=True)
    
    skill = models.ForeignKey(Skill, related_name="added_skills", verbose_name=_('Skill'), null=True)
    skill_details = property(lambda _s: _s.skill.details)
    rate = models.PositiveIntegerField(_('Rate of Activation'), null=True)

    DEPENDENCY_CHOICES = (
        ('notes', _('notes')),
        ('PERFECTs'),
        ('time', _('seconds')),
        ('combo', _('x combo')),
    )
    i_dependency = models.PositiveIntegerField(_('Dependency'), choices=i_choices(DEPENDENCY_CHOICES), null=True)
    
    chance = models.PositiveIntegerField(_('% Chance'), null=True)
    number = models.PositiveIntegerField('{number}', null=True)
    length = models.PositiveIntegerField('{length}', null=True)

    SKILL_REPLACE = (
        'rate',
        'dependency',
        'chance',
        'number',
        'length',
    )

    IDOL_REPLACE = (
        'unit',
        'subunit',
        'year',
    )

    CENTERS = OrderedDict([
        ('princess', {
            'translation': _('Princess'),
            'focus': 'smile',
            'on_attribute': _(u'{} pts. up by +9%'),
            'off_attribute': _(u'{} pts. up by +12% of Smile'),
        }),
        ('angel', {
            'translation': _('Angel'),
            'focus': 'pure',
            'on_attribute': _(u'{} pts. up by +9%'),
            'off_attribute': _(u'{} pts. up by +12% of Pure'),
        }),
        ('empress', {
            'translation': _('Empress'),
            'focus': 'cool',
            'on_attribute': _(u'{} pts. up by +9%'),
            'off_attribute': _(u'{} pts. up by +12% of Cool'),
        }),
        ('star', {
            'translation': _('Star'),
            'on_attribute': _(u'{} pts. up by 7%'),
        }),
        ('heart', {
            'translation': _('Heart'),
            'on_attribute': _(u'{} pts. up by +6%'),
        }),
        ('energy', {
            'translation': _('Energy'),
            'on_attribute': _(u'{} pts. up by +4%'),
        }),
        ('power', {
            'translation': _('Power'),
            'on_attribute': _(u'{} pts. up by +3%'),
        }),
        ])
            
    CENTER_CHOICES = [(_name, _info['translation']) for _name, _info in CENTERS.items()]
    i_center = models.PositiveIntegerField(_('Center Skill'), choices=i_choices(CENTER_CHOICES), null=True)
    center_focus = property(getInfoFromChoices('center', CENTERS, 'focus'))
    center_off_attribute = property(getInfoFromChoices('center', CENTERS, 'off_attribute'))
    center_on_attribute = property(getInfoFromChoices('center', CENTERS, 'on_attribute'))

    OFF_ATTRIBUTE_CENTERS = ['princess', 'angel', 'empress']

    @property
    def center_details(self):
        if self.center in self.OFF_ATTRIBUTE_CENTERS and self.attribute != self.center_focus:
            return self.center_off_attribute 
        return self.center_on_attribute

    GROUP_BOOST = (
        ('unit', _('Unit')),
        ('subunit', _('Subunit')),
        ('year', _('Year')),
    )
    i_group = models.PositiveIntegerField(_('Boost Group'), choices=i_choices(GROUP_BOOST), null=True)
    boost_percent = models.PositiveIntegerField(_('Boost Percentage'), null=True)

    image = models.ImageField(_('Image'), upload_to=uploadItem('c'), null=True)
    image_idol = models.ImageField(string_concat(_('Image'), ' (', _('Idolized'), ')'), upload_to=uploadItem('c'), null=True)

    old_image = models.ImageField(string_concat(_('Image'), ' (', _('Old'), ')'), upload_to=uploadItem('c'), null=True)
    old_image_idol = models.ImageField(string_concat(_('Image'), ' (', _('Old'), ', ', _('Idolized'), ')'), upload_to=uploadItem('c'), null=True)

    icon = models.ImageField(_('Icon'), upload_to=uploadItem('c'), null=True)
    icon_idol = models.ImageField(string_concat(_('Icon'), ' (', _('Idolized'), ')'), upload_to=uploadItem('c'), null=True)

    old_icon = models.ImageField(string_concat(_('Icon'), ' (', _('Old'), ')'), upload_to=uploadItem('c'), null=True)
    old_icon_idol = models.ImageField(string_concat(_('Icon'), ' (', _('Old'), ', ', _('Idolized'), ')'), upload_to=uploadItem('c'), null=True)

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c'), null=True)
    transparent_idol = models.ImageField(string_concat(_('Transparent'), ' (', _('Idolized'), ')'), upload_to=uploadItem('c'), null=True)

    art = models.ImageField(_('Art'), upload_to=uploadItem('c'), null=True)
    art_idol = models.ImageField(string_concat(_('Art'), ' (', _('Idolized'), ')'), upload_to=uploadItem('ic'), null=True)

    old_art = models.ImageField(string_concat(_('Art'), ' (', _('Old'), ')'), upload_to=uploadItem('c'), null=True)
    old_art_idol = models.ImageField(string_concat(_('Art'), ' (', _('Old'), ', ', _('Idolized'), ')'), upload_to=uploadItem('ic'), null=True)

    smile_min = models.PositiveIntegerField(string_concat(_('Smile'), ' (', _('Minimum'), ')'), null=True)
    smile_max = models.PositiveIntegerField(string_concat(_('Smile'), ' (', _('Maximum'), ')'), null=True)
    smile_max_idol = models.PositiveIntegerField(string_concat(_('Smile'), ' (', _('Idolized'), ', ', _('Maximum'), ')'), null=True)

    pure_min = models.PositiveIntegerField(string_concat(_('Pure'), ' (', _('Minimum'), ')'), null=True)
    pure_max = models.PositiveIntegerField(string_concat(_('Pure'), ' (', _('Maximum'), ')'), null=True)
    pure_max_idol = models.PositiveIntegerField(string_concat(_('Pure'), ' (', _('Idolized'), ', ', _('Maximum'), ')'), null=True)

    cool_min = models.PositiveIntegerField(string_concat(_('Cool'), ' (', _('Minimum'), ')'), null=True)
    cool_max = models.PositiveIntegerField(string_concat(_('Cool'), ' (', _('Maximum'), ')'), null=True)
    cool_max_idol = models.PositiveIntegerField(string_concat(_('Cool'), ' (', _('Idolized'), ', ', _('Maximum'), ')'), null=True)

    hp = models.PositiveIntegerField(string_concat(_('HP'), ' (', _('Unidolized'), ')'), null=True)

    in_set = models.ForeignKey(Set, related_name="sets", verbose_name=_('Sets'), null=True)

    details = models.TextField(_('Details'), null=True)
    DETAILSS_CHOICES = ALL_ALT_LANGUAGES
    d_detailss = models.TextField(null=True)
    
############################################################
# Events

class Event(MagiModel):
    collection_name = 'event'
    owner = models.ForeignKey(User, related_name='added_events')

    title = models.CharField(_('Title'), max_length=100)
    TITLES_CHOICES = ALL_ALT_LANGUAGES
    d_titles = models.TextField(null=True)

    def __unicode__(self):
        return u'{}'.format(self.t_title)

    banner = models.ImageField(_('Banner'), upload_to=uploadItem('e'), null=True)

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

    jp_banner = models.ImageField(string_concat(t['Japanese'], ' ', _('version'), '-',_('Banner')), upload_to=uploadItem('e'), null=True)
    jp_start_date = models.DateTimeField(string_concat(t['Japanese'], ' ', _('version'), ' - ', _('Beginning')), null=True)
    jp_end_date = models.DateTimeField(string_concat(t['Japanese'], ' ', _('version'), ' - ',_('End')), null=True)

    ww_banner = models.ImageField(string_concat(_('Worldwide'), ' ', _('version'), '-',_('Banner')), upload_to=uploadItem('e'), null=True)
    ww_start_date = models.DateTimeField(string_concat(_('Worldwide'), ' ', _('version'), ' - ', _('Beginning')), null=True)
    ww_end_date = models.DateTimeField(string_concat(_('Worldwide'), ' ', _('version'), ' - ',_('End')), null=True)

    tw_banner = models.ImageField(string_concat(_('Taiwanese'), ' ', _('version'), '-',_('Banner')), upload_to=uploadItem('e'), null=True)
    tw_start_date = models.DateTimeField(string_concat(_('Taiwanese'), ' ', _('version'), ' - ', _('Beginning')), null=True)
    tw_end_date = models.DateTimeField(string_concat(_('Taiwanese'), ' ', _('version'), ' - ',_('End')), null=True)

    kr_banner = models.ImageField(string_concat(_('Korean'), ' ', _('version'), '-',_('Banner')), upload_to=uploadItem('e'), null=True)
    kr_start_date = models.DateTimeField(string_concat(_('Korean'), ' ', _('version'), ' - ', _('Beginning')), null=True)
    kr_end_date = models.DateTimeField(string_concat(_('Korean'), ' ', _('version'), ' - ',_('End')), null=True)

    cn_banner = models.ImageField(string_concat(_('Chinese'), ' ', _('version'), '-',_('Banner')), upload_to=uploadItem('e'), null=True)
    cn_start_date = models.DateTimeField(string_concat(_('Chinese'), ' ', _('version'), ' - ', _('Beginning')), null=True)
    cn_end_date = models.DateTimeField(string_concat(_('Chinese'), ' ', _('version'), ' - ',_('End')), null=True)

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
