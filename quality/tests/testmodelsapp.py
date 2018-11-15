from django.test import TestCase
from quality.models import Product, Backup, SubstitutProduct
from django.apps import apps
from quality.apps import QualityConfig


class ProductModelTest(TestCase):
    def test_string_representation(self):
        product = Product(name='Nutella')
        self.assertEqual(str(product), product.name)

class BackupModelTest(TestCase):
    def test_string_representation(self):
        backup = Backup(id=1)
        self.assertEqual(str(backup), str(backup.id))

class SubstitutProductModelTest(TestCase):
    def test_string_representation(self):
        product = SubstitutProduct(name='Pate à Tartiner')
        self.assertEqual(str(product), product.name)


class QualityConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(QualityConfig.name, 'quality')
        self.assertEqual(apps.get_app_config('quality').name , 'quality')