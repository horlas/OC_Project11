import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from .create_fixture import fill_database
from quality.models import Product
from django.core.management.commands import loaddata

class Command(BaseCommand):
    help = 'fill data base with a OFF Categorie'

    def add_arguments(self, parser):
        parser.add_argument('categories', nargs='+', type=str)

    def handle(self, *args, **options):
        for category in options['categories']:
            nb_products = fill_database(category)
            #test the fixture is well created
            content = os.path.getsize('quality/fixtures/dugras_data.json')
            if content != 0 :
                self.stdout.write(self.style.SUCCESS('Successfully created fixtures for the category {} '.format(category)))
            else:
                self.stdout.write(self.style.WARNING('Le fichier de fixture est vide'))

            self.stdout.write(self.style.NOTICE('Vous vous préparez à charger {} en base'.format(nb_products)))

            #test if products well loaded in database:
            count_before = Product.objects.count()
            call_command('loaddata', 'dugras_data.json', verbosity=0)
            count_after = Product.objects.count()
            if count_before + nb_products == count_after:
                self.stdout.write(
                    self.style.SUCCESS('Successfully loaded fixtures for the category {} '.format(category)))
            else :
                self.stdout.write(self.style.WARNING('A problem occurs'))
