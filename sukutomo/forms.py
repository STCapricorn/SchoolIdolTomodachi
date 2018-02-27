import datetime
from magi import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from magi.utils import PastOnlyValidator
from magi.forms import AutoForm
from sukutomo import models

class AccountForm(forms.AccountForm):
    start_date = forms.forms.DateField(required=False, label=_('Start Date'), validators=[
        PastOnlyValidator,
        MinValueValidator(datetime.date(2013, 4, 16)),
    ])

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        if 'fake' in self.fields:
            del(self.fields['fake'])
        if 'transfer_code' in self.fields:
            del(self.fields['transfer_code'])
        if 'nickname' in self.fields and self.request.user.is_authenticated():
            self.fields['nickname'].initial = self.request.user.username

    class Meta(forms.AccountForm.Meta):
        optional_fields = ('level', 'friend_id', 'accept_friend_requests', 'device', 'start_date',
                           'loveca', 'friend_points', 'g', 'tickets', 'vouchers', 'bought_loveca',
                           'i_play_with', 'i_os')

class IdolForm(AutoForm):
    class Meta:
        model = models.Idol
        optional_fields = ('japanese_name', 'image', 'i_attribute', 'i_unit', 'i_subunit', 'age',
                           'birthday', 'i_astrological_sign', 'i_blood', 'height', 'bust', 'waist', 'hips', 'hobbies',
                           'favorite_food', 'least_favorite_food', 'description')
            
