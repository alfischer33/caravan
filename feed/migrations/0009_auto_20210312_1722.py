# Generated by Django 3.1.7 on 2021-03-13 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20210312_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventdestination',
            name='hostel_ptr',
        ),
        migrations.RemoveField(
            model_name='hosteldestination',
            name='hostel_ptr',
        ),
        migrations.DeleteModel(
            name='AreaDestination',
        ),
        migrations.DeleteModel(
            name='EventDestination',
        ),
        migrations.DeleteModel(
            name='HostelDestination',
        ),
    ]
