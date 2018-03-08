from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection
from django.utils.translation import ugettext_lazy as _
from magi.utils import CuteFormType, CuteFormTransform
from sukutomo import forms, models
from magi.utils import staticImageURL

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm

    filter_cuteform = {
        'accept_friend_requests': {
            'type': CuteFormType.YesNo,
        },
        'i_play_with': {
            'to_cuteform': lambda k, v: models.Account.PLAY_WITH[models.Account.get_reverse_i('play_with', k)]['icon'],
            'transform': CuteFormTransform.FlaticonWithText,
        },
        'i_version': {
            'to_cuteform': lambda k, v: models.Account.VERSIONS[models.Account.get_reverse_i('version', k)]['icon'],
            'transform': CuteFormTransform.FlaticonWithText,
        },
        'i_os': {
            'transform': CuteFormTransform.FlaticonWithText,
        },
    }

    class ListView(_AccountCollection.ListView):
        pass

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    title = _('Idol')
    plural_title = _('Idols')
    multipart = True
    form_class = forms.IdolForm

    def to_fields(self, view, item, *args, **kwargs):
        # Call the super, provide icons and images
        fields = super(IdolCollection, self).to_fields(view, item, *args, icons={
            'name': 'id',
            'japanese_name': 'id',
            'age': 'scoreup',
            'birthday': 'event',
            'height': 'scoreup',
            'blood': 'hp',
            'bust': 'id',
            'waist': 'id',
            'hips': 'id',
            'hobbies': 'star',
            'favorite_food': 'heart',
            'least_favorite_food' : 'heart-empty',
            'description': 'id',
        }, images={
            'attribute': staticImageURL(item.i_attribute, folder='i_attribute', extension='png'),
            'unit': staticImageURL(item.i_unit, folder='i_unit', extension='png'),
            'subunit': staticImageURL(item.i_subunit, folder='i_subunit', extension='png'),
            'astrological_sign': staticImageURL(item.i_astrological_sign, folder='i_astrological_sign', extension='png'),
        }, **kwargs)
                                                       
        return fields

