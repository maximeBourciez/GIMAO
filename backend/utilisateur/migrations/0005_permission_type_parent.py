from django.db import migrations, models
import django.db.models.deletion

from tasks.perms_data import perms


def populate_type_and_parent(apps, schema_editor):
    Permission = apps.get_model('utilisateur', 'Permission')

    # Premier passage : mettre à jour le type
    for nom, (description, perm_type, parent_nom) in perms.items():
        Permission.objects.filter(nomPermission=nom).update(type=perm_type)

    # Deuxième passage : assigner le parent (toutes les perms existent déjà)
    for nom, (description, perm_type, parent_nom) in perms.items():
        if parent_nom:
            try:
                perm = Permission.objects.get(nomPermission=nom)
                parent = Permission.objects.get(nomPermission=parent_nom)
                perm.parent = parent
                perm.save()
            except Permission.DoesNotExist:
                pass


def remove_type_and_parent(apps, schema_editor):
    Permission = apps.get_model('utilisateur', 'Permission')
    Permission.objects.update(type='action', parent=None)


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0004_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='type',
            field=models.CharField(
                choices=[('affichage', 'Affichage'), ('action', 'Action')],
                default='action',
                help_text='Type de permission : affichage (lecture) ou action (écriture)',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='permission',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                help_text='Permission parente : si cochée, cette permission est automatiquement activée',
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='enfants',
                to='utilisateur.permission',
            ),
        ),
        migrations.RunPython(populate_type_and_parent, remove_type_and_parent),
    ]
