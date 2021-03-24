# Generated by Django 3.1.7 on 2021-03-15 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0012_caravan_invisible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stop',
            old_name='hostel',
            new_name='destination',
        ),
        migrations.AlterField(
            model_name='caravan',
            name='age_range',
            field=models.CharField(choices=[('18-25', '18-23'), ('25-29', '23-29'), ('30-39', '30-39'), ('40-65', '40-65'), ('65+', '65+'), ('family', 'Family'), ('any', 'All Ages')], max_length=15),
        ),
        migrations.AlterField(
            model_name='caravan',
            name='duration',
            field=models.CharField(choices=[('event', 'Event'), ('journey', 'Journey'), ('nomadic', 'Nomadic'), ('other', 'Other')], max_length=15),
        ),
        migrations.AlterField(
            model_name='caravan',
            name='mood',
            field=models.CharField(choices=[('party', 'Party'), ('enjoy', 'Enjoy'), ('explore', 'Explore'), ('volunteer', 'Volunteer'), ('work', 'Work'), ('other', 'Other')], max_length=15),
        ),
    ]
