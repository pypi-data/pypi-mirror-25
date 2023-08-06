from django.core.management import BaseCommand

from ws4ever.backend import notify_clients


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('kind', help='message kind')
        parser.add_argument('payload', help='message payload')

    def handle(self, **options):
        kind = options['kind']
        payload = options['payload']

        notify_clients(kind, payload)
        self.stdout.write('Broadcasted!')
        self.stdout.write('- kind: {}'.format(kind))
        self.stdout.write('- payload: {}'.format(payload))
