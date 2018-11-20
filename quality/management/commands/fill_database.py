import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from .create_fixture import fill_database
from quality.models import Product
from django.db.models import Count, Max


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

            self.stdout.write(self.style.NOTICE('You are preparing to load {} in data base'.format(nb_products)))

            #test if products well loaded in database:
            count_before = Product.objects.count()
            call_command('loaddata', 'dugras_data.json', verbosity=0)
            count_after = Product.objects.count()
            if count_before + nb_products == count_after:
                self.stdout.write(
                    self.style.SUCCESS('Successfully loaded fixtures for the category {} '.format(category)))
            else :
                self.stdout.write(self.style.WARNING('A problem occurs'))

            # Removes records from `Product` duplicated on `name`
            # while leaving the most recent one (biggest `id`).
            # value: return a dictionnary
            # annotate : nombre de repetition du nom
            # __gt=1 : get all entries with more than one occurence
            # source : https://stackoverflow.com/questions/13700200/remove-duplicates-in-django-orm-multiple-rows/13700642#13700642
            self.stdout.write(self.style.NOTICE('Deleting products with the same name'))

            duplicates = Product.objects.values('name').order_by().annotate(max_id=Max('id') ,
                                                                            count_id=Count('id')).filter(count_id__gt=1)
            fields =['name']
            for duplicate in duplicates:
                Product.objects.filter(**{x: duplicate[x] for x in fields}).exclude(id=duplicate['max_id']).delete()
            #
            count_after_delete_duplicates = Product.objects.count()
            self.stdout.write(self.style.SUCCESS('{} products have been deleted'.format((count_after - count_after_delete_duplicates))))

# categories
# categories = ['Pâtes à tartiner aux noisettes et au cacao',
#  'Pizzas au jambon',
#  'Plats préparés surgelés',
#  "Chips à l'ancienne",
#  'Purées de pommes de terre',
#  'Margarines allégées'
#  'Farines',
#  'Desserts au soja'
#  'Snacks sucrés'
#
#  'Viennoiseries'
#  'Plats préparés'
#   'Sauces'
#   'Charcuteries à cuire']