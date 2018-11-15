import random
from django.utils.translation import ugettext_lazy as _

def generateDifficulty(rating, notes):
    string = _('{} &#9734 rating').format(rating) if rating != None else ''
    string+='<br />' if string != '' else ''
    string+=_('{} notes').format(notes) if notes != None else ''
    return string


