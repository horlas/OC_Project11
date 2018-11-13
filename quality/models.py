from django.conf import settings
from django.db import models
# Create your models here.

class TimestamptedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

class Product(models.Model):
    name = models.CharField(max_length=250)
    url = models.URLField()
    img = models.URLField()
    n_grade = models.CharField(max_length=2)
    category = models.CharField(max_length=250)
    img_nutrition = models.URLField(default='0000000')
    store = models.CharField(max_length=250 , default='0000000')

    class Meta:
        verbose_name = "product"

    def __str__(self):
        return self.name

class Backup(TimestamptedModel):
    selected_product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "backup"

    def __str__(self):
        return str(self.id)



class SubstitutProduct(models.Model):
    name =  models.CharField(max_length=250)
    url = models.URLField()
    img = models.URLField()
    n_grade = models.CharField(max_length=1)
    category = models.CharField(max_length=250)
    img_nutrition = models.URLField(default='0000000')
    store = models.CharField(max_length=250, default='0000000')
    backup_id = models.ForeignKey(Backup , on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "substitut_product"

    def __str__(self):
        return self.name



