# Generated by Django 5.2 on 2025-04-23 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monarque', '0003_alter_menu_actif_alter_plat_actif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='prenom',
            field=models.CharField(max_length=50, verbose_name='Prenom Chef'),
        ),
        migrations.AlterField(
            model_name='liensociale',
            name='designation',
            field=models.CharField(max_length=50, verbose_name='Nom de la Plateforme'),
        ),
        migrations.AlterField(
            model_name='liensociale',
            name='lien',
            field=models.CharField(max_length=255, unique=True, verbose_name='lien vers le compte'),
        ),
        migrations.AlterField(
            model_name='liensociale_company',
            name='designation',
            field=models.CharField(max_length=50, verbose_name='Nom de la Plateforme'),
        ),
        migrations.AlterField(
            model_name='liensociale_company',
            name='lien',
            field=models.CharField(max_length=255, unique=True, verbose_name='lien vers le compte'),
        ),
    ]
