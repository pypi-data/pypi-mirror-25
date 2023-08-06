import json
from pprint import pformat

from django.core.management import BaseCommand

from ws4ever.backend import notify_clients


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', action='store_false',
            dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.')
        parser.add_argument('kind', help='message kind')
        parser.add_argument('payload', help='message payload')

    def handle(self, **options):
        kind = options['kind']
        try:
            payload = json.loads(options['payload'])
        except:
            payload = options['payload']

        self.stdout.write('\nkind: \n{}'.format(kind))
        self.stdout.write('\npayload: \n{}'.format(pformat(payload)))

        if options.get('interactive'):
            input('\ncontinue?')

        notify_clients(kind, payload)
