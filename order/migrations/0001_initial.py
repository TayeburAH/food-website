# Generated by Django 3.2 on 2021-05-13 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(null=True)),
                ('total_quantity', models.PositiveIntegerField(null=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Pending', 'Pending')], default='Not confirmed', max_length=14)),
                ('total', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('cancel_reason', models.CharField(blank=True, max_length=200, null=True)),
                ('order_id', models.CharField(blank=True, max_length=120, null=True)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('cash', models.CharField(max_length=10, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.customer')),
            ],
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('size', models.CharField(max_length=2, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('orderplaced', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderplaced')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.product')),
            ],
        ),
    ]
