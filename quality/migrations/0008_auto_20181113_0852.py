# Generated by Django 2.0 on 2018-11-13 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quality', '0007_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='selected_product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quality.Product'),
        ),
        migrations.AlterField(
            model_name='substitutproduct',
            name='selected_product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quality.Product'),
        ),
        migrations.DeleteModel(
            name='SelectedProduct',
        ),
    ]