# Generated by Django 4.1.4 on 2022-12-09 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('litleLemonAPI', '0003_alter_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='litleLemonAPI.category'),
        ),
    ]
