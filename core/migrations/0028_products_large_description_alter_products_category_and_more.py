# Generated by Django 4.1.3 on 2022-11-14 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_products_name_alter_products_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='large_description',
            field=models.TextField(help_text='Descripcion larga del producto del producto', max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(help_text='Categoria del producto', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='core.category'),
        ),
        migrations.AlterField(
            model_name='products',
            name='condition',
            field=models.CharField(choices=[('NEW', 'Nuevo'), ('USED', 'Usado'), ('REFURBISHED', 'Remanufacturado')], default='NEW', help_text='Condicion del producto', max_length=50),
        ),
        migrations.AlterField(
            model_name='products',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha de creacion del producto'),
        ),
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(help_text='Descripcion corta del producto', max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0, help_text='Porcentaje de descuento de un producto, en caso de que lo tenga.'),
        ),
        migrations.AlterField(
            model_name='products',
            name='photos',
            field=models.ManyToManyField(help_text='Fotos y/o archivos asociados al producto', to='core.media'),
        ),
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.PositiveBigIntegerField(help_text='Cantidad del producto en inventario'),
        ),
        migrations.AlterField(
            model_name='products',
            name='thumbnail',
            field=models.ImageField(help_text='Miniatura del producto', upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Fecha de actualizacion del producto'),
        ),
    ]