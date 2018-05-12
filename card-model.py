from magi.item_model import MagiModel
from magi.models import User, uploadItem, Idol, AccountAsOwnerModel

class Card(MagiModel):
    collection_name = 'card'
    RAREITY_CHOICES = (
    'N'#possibly list with level caps?
    'R'    
    'SR' 
    'SSR'
    'UR'
    'Promo R'
    'Promo SR'
    'Promo UR'
    )
    ATTRIBUTE_CHOICES = (
    'Smile'
    'Pure'
    'Cool'
    'All'
    )
    SKILL_CHOICES = (
    'Score Up'
    'Perfect Lock'
    'Stamina Recovery'
    'No Skill'
    )
    #many too many
    owner = models.ForeignKey(User, related_name='cards')
    account = models.ForeignKey(Account, related_name='ownedcards')
    title = models.CharField(_('Title'), max_length=100, unique=True)
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    rareity = models.PositiveIntegerField(_('Rareity'), choices=i_choices(RAREITY_CHOICES), null=True)
    num = models.PositiveIntegerField(_('Card #ID'), blank=True, unique=True)
    date = models.DateField(_('Release Date')
    collection = #i guess each set is a collection, hmmmmm
    idol = #model field???? lmao
    skill-name = models.CharField(_('Skill Name'), max_length=100, unique=True)
    skill-typ = models.PositiveIntegerField(_('Skill'), choices=i_choices(SKILL_CHOICES), null=True)
    #skill types have specific decriptions hmmmm           
    center-name = #choice field
    #skill types have specific decriptions hmmmm                        
    #if veiwing as idolized max hp++ or smth, need something to toggle view
    hp = models.PositiveIntegerField(_('HP'), blank=True, null=True))
    initial-s-points = models.PositiveIntegerField(_('Smile Points'),#can these have the same name?
    maxUnidol-s-points = models.PositiveIntegerField(_('Smile Points'), 
    maxIdol-s-points = models.PositiveIntegerField(_('Smile Points'), 
    initial-p-points = models.PositiveIntegerField(_('Pure Points'), 
    maxUnidol-p-points = models.PositiveIntegerField(_('Pure Points'), 
    maxIdol-p-points = models.PositiveIntegerField(_('Pure Points'), 
    initial-c-points = models.PositiveIntegerField(_('Cool Points'), 
    maxUnidol-c-points = models.PositiveIntegerField(_('Cool Points'), 
    maxIdol-c-points = models.PositiveIntegerField(_('Cool Points'),
    isEvent = #enter a boolean value, or just make it a choice
    if(isEvent)
        #event model shenanigans                                    
    #toggle image download views                         
    if rareity == SSR || rareity == UR 
        pair =
    if rareity != Promo SR || rareity != Promo UR || rareity != Promo R
        clean-unidol =
        transp-unidol =
    clean-idol =
    transp-idol =
    sources = #paragrah feild
    #how to structure disquis comments... if we arent on the car page it has the amount otherwise the actual commebts
    comments =
    japanOnly = #enter a boolean value, or just make it a choice
    isPromo = #enter a boolean value, or just make it a choice

    #get methods *KEYBOARD SMASH*
    def __unicode__(self):
        return self.name
