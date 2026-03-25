from django.db import migrations, models
import django.db.models.deletion


MODULES = {
    'di': "Demandes d'intervention",
    'bt': 'Bons de travail',
    'eq': 'Équipements',
    'cp': 'Compteurs',
    'mp': 'Maintenances préventives',
    'stock': 'Stocks',
    'cons': 'Consommables',
    'mag': 'Magasins',
    'user': 'Utilisateurs',
    'role': 'Rôles',
    'loc': 'Lieux',
    'sup': 'Fournisseurs',
    'man': 'Fabricants',
    'eqmod': "Modèles d'équipement",
    'export': 'Export',
    'menu': 'Menu',
    'dash': 'Dashboard',
}


def populate_modules(apps, schema_editor):
    Module = apps.get_model('utilisateur', 'Module')
    Permission = apps.get_model('utilisateur', 'Permission')

    modules = {}
    for code, nom in MODULES.items():
        module, _ = Module.objects.get_or_create(code=code, defaults={'nom': nom})
        modules[code] = module

    for perm in Permission.objects.all():
        code = perm.nomPermission.split(':')[0]
        if code in modules:
            perm.module = modules[code]
            perm.save()


def remove_modules(apps, schema_editor):
    Permission = apps.get_model('utilisateur', 'Permission')
    Permission.objects.update(module=None)
    Module = apps.get_model('utilisateur', 'Module')
    Module.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0003_alter_role_options_remove_role_rang'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Code court du module (ex: di, bt, eq)', max_length=20, unique=True)),
                ('nom', models.CharField(help_text='Nom lisible du module (ex: Demandes d\'intervention)', max_length=100)),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
                'db_table': 'gimao_module',
                'ordering': ['nom'],
            },
        ),
        migrations.AddField(
            model_name='permission',
            name='module',
            field=models.ForeignKey(
                blank=True,
                null=True,
                help_text='Module auquel appartient cette permission',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='permissions',
                to='utilisateur.module',
            ),
        ),
        migrations.RunPython(populate_modules, remove_modules),
    ]
