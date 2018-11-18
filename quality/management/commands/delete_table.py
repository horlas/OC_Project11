from django.core.management.base import BaseCommand
from quality.models import Product, SubstitutProduct, Backup

class Command(BaseCommand):
    help = 'Delete a specificate database table'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete all table',
        )

    def handle(self, *args, **options):

        table_1 = Product.objects.all()
        table_2 = SubstitutProduct.objects.all()
        table_3 = Backup.objects.all()


        if options['delete']:
            table_1.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  Product table '))
            table_2.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  SubstitutProduct table '))
            table_3.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  Backup table '))