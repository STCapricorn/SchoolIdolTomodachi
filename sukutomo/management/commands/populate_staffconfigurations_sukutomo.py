from django.core.management.base import BaseCommand, CommandError
from magi.utils import LANGUAGES_DICT
from magi.management.commands.populate_staffconfigurations import create
from sukutomo import models

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):

        # Event Times
        for _name, _info in models.Account.VERSIONS.items():
            for timing in ['start', 'end']:
                for unit in ['hour', 'minute']:
                    create({
                        'key': 'event_{version}_{timing}_{unit}'.format(version=_name, timing=timing, unit=unit),
                        'verbose_key': 'Event: {version} {timing} ({unit})'.format(
                        version=unicode(_info['translation']), timing=timing, unit=unit),
                        'is_long': True,
                    })

        # Song Times        
        for field in ['release', 'b_side_start', 'b_side_end']:
            for unit in ['hour', 'minute']:
                create({
                    'key': 'song_{field}_{unit}'.format(field=field, unit=unit),
                    'verbose_key': 'Song: {field} ({unit})'.format(field=field, unit=unit),
                    'is_long': True,
                })
