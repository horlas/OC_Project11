from django.core.management import call_command
from django.core.management.base import BaseCommand
from .create_fixture import fill_database
from quality.models import Product, SubstitutProduct, Backup
from django.contrib.auth.models import User
from django.db.models import Count, Max
import datetime


class Command(BaseCommand):
    help = 'get some information from database'

    def handle(self , *args , **options):

        #how many pur_beurre users?
        self.stdout.write(self.style.SUCCESS('How many Users ? : '))
        self.stdout.write(self.style.NOTICE('{}'.format(User.objects.filter(is_active=1).count())))
        #how many superusers?
        superusers = User.objects.filter(is_superuser=1).values('username', 'last_login')
        count_superuser = superusers.count()
        self.stdout.write(self.style.SUCCESS('How many superusers ? '))
        self.stdout.write(self.style.NOTICE('{}'.format(count_superuser)))
        for superuser in superusers:
            self.stdout.write(self.style.SUCCESS('Who ? '))
            self.stdout.write(self.style.NOTICE('{}'.format(superuser['username'])))

            date = superuser['last_login']
            self.stdout.write(self.style.SUCCESS('When did he connect for last time ? : '))
            self.stdout.write(self.style.NOTICE(
                '{}'.format(date.strftime('%d %B, %Y à %H:%M:%S'))))
        # how many Products in database? and how many categorie ?

        self.stdout.write(self.style.SUCCESS('How many products in database ?'))
        self.stdout.write(self.style.NOTICE('{}'.format(Product.objects.count())))


        # how many Category and how many products per category
        query = Product.objects.all().values('category').annotate(total=Count('category')).order_by('-total')
        self.stdout.write(self.style.SUCCESS('How many category ? '))
        self.stdout.write(self.style.NOTICE('{}'.format(
            query.count())))


        self.stdout.write(self.style.SUCCESS('How many products in the first ten category ? : '))
        for c in query[:10] :
            self.stdout.write(self.style.NOTICE('category : {}  nb_products : {} '.format(c['category'], c['total'])))

        # how many Backups
        self.stdout.write(self.style.SUCCESS('How many backups in database ? '))
        self.stdout.write(self.style.NOTICE('{}'.format(Backup.objects.count())))

        # which name of the user who made the most backups
        # select username where
        # select username where user_id=3 from user
        self.stdout.write(self.style.SUCCESS("Name of the user who made the most backups"))
        q = Backup.objects.values('user_id').annotate(Count('id')).order_by('-id__count')[:1]
        for a, b in enumerate(q):
            user = User.objects.get(id=b['user_id'])
            self.stdout.write(self.style.NOTICE("nom de l'utilisateur : {}".format(user.username)))


            self.stdout.write(self.style.NOTICE('nombre de sauvegardes : {} '.format(b['id__count'])))


        # how many substitut products

        self.stdout.write(self.style.SUCCESS('How many substituts products in database ? '))
        self.stdout.write(self.style.NOTICE('{}'.format(SubstitutProduct.objects.count())))



