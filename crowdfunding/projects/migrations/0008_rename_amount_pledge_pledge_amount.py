# Generated by Django 4.1.5 on 2023-01-25 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_project_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pledge',
            old_name='amount',
            new_name='pledge_amount',
        ),
    ]