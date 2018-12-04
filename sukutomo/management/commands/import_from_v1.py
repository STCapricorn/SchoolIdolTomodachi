import requests, json
from pprint import pprint
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from magi.utils import modelHasField
from sukutomo import models

settings = None

def import_map(maps, field_name, value):
    if not isinstance(maps, list):
        maps = [maps]
    fields = None
    for mapped in maps:
        # Dict of values -> new values
        if isinstance(mapped, dict):
            value = mapped.get(value, value)
        # Function to get value
        elif callable(mapped):
            result = mapped(value)
            # Function can return multiple fields in a dict
            if isinstance(result, dict):
                fields = result
            # Or return a new field_name and a value
            else:
                field_name, value = result
        # If the new field name is a dict, add to the dict
        elif mapped.startswith('d_'):
            value = { field_name: value }
            field_name = mapped
        # Or map can just change the field_name
        else:
            field_name = mapped
    return fields if fields is not None else { field_name: value }

def import_generic_item(details, item):
    data = {}
    unique_data = {}
    all_fields = details.get('fields', []) + details.get('unique_fields', [])
    not_in_fields = {}
    for field_name, value in item.items():

        fields = { field_name: value }

        # Map
        if field_name in details.get('mapping', {}):
            fields = import_map(details['mapping'][field_name], field_name, value)

        elif field_name not in all_fields:
            not_in_fields[field_name] = value
            continue

        for field_name, value in fields.items():
            # Get i_choices if field name is i_
            if field_name.startswith('i_'):
                for i, choice in details['model'].get_choices(field_name):
                    choice = choice[0] if isinstance(choice, tuple) else choice
                    if value == choice:
                        value = i
                        break
            # Push to unique fields or normal fields
            if field_name in details.get('unique_fields', ['id']):
                unique_data[field_name] = value
            else:
                # Update existing dictionaries
                if (field_name.startswith('d_')
                    and isinstance(value, dict)
                    and field_name in data):
                    data[field_name].update(value)
                else:
                    data[field_name] = value

    if 'callback' in details:
        details['callback'](details, item, unique_data, data)
    return unique_data, data, not_in_fields

def save_item(model, unique_data, data):
    if (data or unique_data):
        for k, v in data.items():
            if k.startswith('d_') and isinstance(v, dict):
                data[k] = json.dumps(v)
        print model.__name__
        print '- Unique data:'
        pprint(unique_data)
        print '- Data:'
        pprint(data)
        data.update(unique_data)
        try:
            item = model.objects.get(reduce(lambda qs, (k, v): qs | Q(**{k: v}), [(k, v) for k, v in unique_data.items() if v is not None], Q()))
            model.objects.filter(pk=item.pk).update(**data)
            print 'Updated'
        except ObjectDoesNotExist:
            if modelHasField(model, 'owner') and 'owner' not in data and 'owner_id' not in data:
                data['owner_id'] = 1
            item = model.objects.create(**data)
            print 'Created'

def api_pages(name, details):
    print 'Downloading list of {}...'.format(name)
    url = 'https://schoolido.lu/api/{}/?page_size=100'.format(details.get('endpoint', name))
    total = 0
    while url:
        if 'local' in settings:
            f = open('{}.json'.format(name), 'r')
            result = json.loads(f.read())
            f.close()
        else:
            r = requests.get(url)
            f = open('{}.json'.format(name), 'w')
            f.write(r.text.encode('utf-8'))
            f.close()
            result = r.json()
        for item in result['results']:
            if item['name'] not in PDP_IDOLS:
                continue
            not_in_fields = {}
            if details.get('generic', True):
                unique_data, data, not_in_fields = import_generic_item(details, item)
            else:
                unique_data, data = details['callback_per_item'](details, item)
            if details.get('callback_per_item', False):
                unique_data, data = details['callback_per_item'](details, item, unique_data, data)
            save_item(details['model'], unique_data, data)
            print '- Ignored:'
            pprint(not_in_fields)
            total += 1
            print '----'
        if 'local' in settings:
            url = None
        else:
            url = result['next']
    details.get('callback_end', lambda: None)()
    print 'Total', total
    print 'Done.'

def download_image(url):
    return url
    # to do download and return image

"""
model (MagiModel): required
endpoint (string)
callback (function)
callback_per_item (function)
end_callback (function)
generic (bool)
mapping (dict of string or callable)
unique_fields (list)
"""

idol_school_choices = {
    unicode(_translation): _id
    for _id, (_short_name, _translation) in models.Idol.get_choices('school')
}
idol_school_choices['Shion Girls Academy'] = idol_school_choices['Shion Girls\' Academy']

def idol_measurements(v):
    if not v:
        return {}
    fields = {}
    for measurement in v.split('/'):
        measurement = measurement.strip()
        if measurement.startswith('B'):
            fields['bust'] = int(measurement[1:])
        elif measurement.startswith('W'):
            fields['waist'] = int(measurement[1:])
        elif measurement.startswith('H'):
            fields['hips'] = int(measurement[1:])
    return fields

def idol_cv(cv):
    if cv:
        cv_unique_data, cv_data, not_in_fields = import_generic_item({
            'unique_fields': ['name'],
            'fields': ['nickname'],
            'mapping': {
                'twitter': 'd_social_media',
                'instagram': 'd_social_media',
            },
        }, cv)
        save_item(models.VoiceActress, cv_unique_data, cv_data)
        print '- Ignored:', not_in_fields
    return {}

PDP_IDOLS = [
    'Tennoji Rina',
    'Yuki Setsuna',
    'Nakasu Kasumi',
    'Uehara Ayumu',
    'Asaka Karin',
    'Ousaka Shizuku',
    'Osaka Shizuku',
    'Emma Verde',
    'Konoe Kanata',
    'Miyashita Ai',
]

def idol_end():
    models.Idol.objects.filter(name__in=PDP_IDOLS).update(
        i_unit=models.Idol.get_i('unit', u'Nijigasaki High School'),
    )

to_import = OrderedDict([
    ('idols', {
        'model': models.Idol,
        'fields': [
            'age', 'height',
            'favorite_food', 'least_favorite_food',
            'hobbies',
        ],
        'mapping': {
            'attribute': lambda v: ('i_attribute', v.lower() if v else None),
            'chibi': lambda v: ('image', download_image(v) if v else None),
            'main_unit': 'i_unit',
            'sub_unit': ['i_subunit', { 'Bibi': 'BiBi', 'Saint Snow': None, 'A-RISE': None }],
            'school': ['i_school', idol_school_choices],
            'year': lambda v: ('i_year', v.lower() if v else None),
            'birthday': lambda v: ('birthday', u'2015-{}'.format(v) if v else None),
            'astrological_sign': lambda v: ('i_astrological_sign', v.lower() if v else None),
            'blood': 'i_blood',
            'measurements': idol_measurements,
            'cv': idol_cv,
            'summary': 'description',
        },
        'unique_fields': ['name', 'japanese_name'],
        'callback_end': idol_end,
    }),
])

def import_from_v1():
    for name, details in to_import.items():
        api_pages(name, details)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        global settings
        settings = args
        import_from_v1()
