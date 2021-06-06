from datetime import datetime

from beautifultable import BeautifulTable
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models import Count, Q
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = 'Shows all superusers login between two dates'

    def add_arguments(self, parser):
        parser.add_argument('date_start', type=str)
        parser.add_argument('date_end', type=str)

    def handle(self, *args, **kwargs):
        start = make_aware(datetime.strptime(kwargs['date_start'], '%Y-%m-%d'))
        end = make_aware(datetime.strptime(kwargs['date_end'], '%Y-%m-%d'))
        users = User.objects.annotate(Count('id')).filter(
            Q(last_login__gte=start) & Q(last_login__lte=end)).order_by('date_joined')

        if not users:
            self.stdout.write("Don't found")
        else:
            table = BeautifulTable()
            table.columns.header = ['id', 'email', 'last_login', 'date_joined']
            self.stdout.write('id email last_login date_joined')
            for user in users:
                table.rows.append([user.id, user.email, '{:%Y-%m-%d}'.format(user.last_login), '{:%Y-%m-%d}'.format(user.date_joined)])
            self.stdout.write(table.get_string())
