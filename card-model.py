#will commit to models.py when its good to go
class Card(MagiModel):

    collection_name = 'card'

    owner = models.ForeignKey(User, related_name='added-cards')

    name = models.CharField(_('Name'), max_length=100, null=True)#removed skill name 

    #if veiwing as idolized max hp++ or smth, need something to toggle view?
    
    initial_smile_points = models.PositiveIntegerField(_('Smile Points'), default=0) 
    max_unidolized_smile_points = models.PositiveIntegerField(_('Smile Points'), default=0)
    max_idolized_smile_points = models.PositiveIntegerField(_('Smile Points'), default=0)
                                                   
    initial_pure_points = models.PositiveIntegerField(_('Pure Points'), default=0)
    max_unidolized_pure_points = models.PositiveIntegerField(_('Pure Points'), default=0)
    max_idolized_pure_points = models.PositiveIntegerField(_('Pure Points'), default=0)
                                                   
    initial_cool_points = models.PositiveIntegerField(_('Cool Points'), default=0)
    max_unidolized__cool_points = models.PositiveIntegerField(_('Cool Points'), default=0)
    max_idolized_cool_points = models.PositiveIntegerField(_('Cool Points'), default=0)

    hp_unidolized = models.PositiveIntegerField(_('HP'), blank=True, default=0)
    hp_idolized = hp_unidolized++ #this doesnt seem like it's allowed in a model, is there a better way besides making another integer field?
    
    RARITY_CHOICES = (
        'N'
        'R'    
        'SR' 
        'SSR'
        'UR'
    )
    
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RAREITY_CHOICES)) #to clarify, this works based on the order and i don't need to make a tuple with and integer correct?
    
    ATTRIBUTE_CHOICES = (
        ('smile', _('Smile')),
        ('pure', _('Pure')),
        ('cool', _('Cool')),
        ('all', _('All')),
    )
    
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=i_choices(ATTRIBUTE_CHOICES))
    
    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='cards')

    date = models.DateField(_('Release Date'), null=True)

    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='event', null=True) #related name okay?

    isPromo = is_promo = models.BooleanField(_('Promo card'), default=False)

    #collection = model.ForeignKey

    #specific detail language style - later commit, not sure how languges and translations work yet
    SKILL_CHOICES = (
        ('score up', _('Score Up')),
        ('perfect lock', _('Perfect Lock')),
        ('stamina recovery', _('Stamina Recovery')),
        ('perfect charm', _('')),
        ('rythmical charm', _('')),
        ('timer charm', _('')),
        ('total charm', _('')),
        ('total trick', _('')),
        ('timer trick', _('')),
        ('perfect yell', _('')),
        ('rythmical yell', _('')),
        ('total yell', _('')),
        ('timer yell', _('')),
        ('appeal boost', _('')),
        ('skill boost', _('')),
        ('combo score up', _('')),
        ('perfect score up', _('')),
        ('amplify', _('')),
        ('encore', _('')),
        ('mirror', _('')),
    )
    
    i_skill = models.PositiveIntegerField(_('Skill'), choices=i_choices(SKILL_CHOICES), null=True)

    #skill decription feilds - later commit

    CENTER_SKILL_CHOICES = (
        ('angel', _('Angel')),
        ('empress', _('Empress')),
        ('princess', _('Princess')),
        ('star', _('Star')),
        ('heart', _('Heart')),
        ('power', _('Power')),
        ('energy', _('Energy')),
    )
    
    i_center_skill = models.PositiveIntegerField(_('Center Skill'), choices=i_choices(CENTER_SKILL_CHOICES), null=True)

    #center skill decription feilds - later commit  
    
    #japan ver choices - later commit
    
    #not sure how uploadItem really works, is it the directory path?
    image_unidolized = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    image_idolized = models.ImageField(_('Idolized Image'), upload_to=uploadItem('i'))
    art_unidolized = models.ImageField(_('Art'), upload_to=uploadItem('i'))
    art_idolized = models.ImageField(_('Idolized Art'), upload_to=uploadItem('i'))
    transparent_unidolized = models.ImageField(_('Transparent'), upload_to=uploadItem('i'))
    transparent_idolized = models.ImageField(_('Idolized Transparent'), upload_to=uploadItem('i'))

    #what other utility functions should i include?
    def __unicode__(self):
        return self.name

