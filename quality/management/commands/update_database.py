################################
# imagine a program that would launch
# every week to register new products
# in the ten smaller categories.
#################################
from django.core.management.base import BaseCommand
from quality.models import Product

from .create_fixture import fill_database
from django.core.management import call_command
from django.db.models import Count, Max
import os

class Command(BaseCommand):
    help = 'get some information from database'

    def handle(self , *args , **options):
        query = Product.objects.all().values('category').annotate(total=Count('category')).order_by('total')

        # just display the ten smallest categories
        self.stdout.write(self.style.SUCCESS('How many products in the last ten category ? : '))
        for c in query[:10]:
            self.stdout.write(self.style.NOTICE('category : {}  nb_products : {} '.format(c['category'], c['total'])))

        for c in query[:10]:
            # we get c['category']
            category = c['category']
            nb_products = fill_database(category)

            # test the fixture is well created
            content = os.path.getsize('quality/fixtures/dugras_data.json')
            if content != 0:
                self.stdout.write(
                    self.style.SUCCESS('Successfully created fixtures for the category {} '.format(category)))
            else:
                self.stdout.write(self.style.WARNING('Le fichier de fixture est vide'))

            self.stdout.write(self.style.NOTICE('You are preparing to load {} products in data base'.format(nb_products)))

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

        # after uploading  smallest categories we delete orphan product
        query_after = Product.objects.all().values('category').annotate(total=Count('category')).filter(total=1)

        # just display the ten smallest categories before delete
        self.stdout.write(self.style.NOTICE('How many category contains just one  product : {}'.format(len(query_after))))

        # delete products
        for product in query_after:
            Product.objects.get(category=product['category']).delete()

        # test
        query_after_delete = Product.objects.all().values('category').annotate(total=Count('category')).filter(total=1)
        if not len(query_after_delete):
            self.stdout.write(self.style.SUCCESS('Orphans category are been deleted '))
        else:
            self.stdout.write(self.style.SUCCESS('Something went wrong'))





