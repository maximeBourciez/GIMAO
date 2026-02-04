from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from decimal import Decimal
import datetime
import json
from .models import Log, Utilisateur
from .middleware import get_current_user

def make_serializable(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    if hasattr(obj, 'pk'):
        return obj.pk
    return obj

@receiver(pre_save)
def capture_old_state(sender, instance, **kwargs):
    # Ignore specific models to prevent clutter or recursion
    if sender._meta.model_name in ['log', 'session', 'contenttype', 'migration', 'adminlog']:
        return
        
    if instance.pk:
        try:
            # We fetch the specific fields to avoid overhead, but model_to_dict needs an instance
            old_instance = sender.objects.get(pk=instance.pk)
            # We manually construct dict to handle non-editable fields if needed, 
            # but model_to_dict is safer for generic use
            instance._old_state = model_to_dict(old_instance)
        except sender.DoesNotExist:
            pass

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender._meta.model_name in ['log', 'session', 'contenttype', 'migration', 'adminlog']:
        return

    # Determine action
    action = 'création' if created else 'modification'
    
    # Calculate changes
    champs_modifies = {}
    
    if created:
        for field in instance._meta.fields:
             try:
                 val = getattr(instance, field.name)
                 # Only log non-empty values for creation to keep log clean? 
                 # Or everything. Let's log everything that is not None/Empty
                 if val not in [None, '']:
                    champs_modifies[field.name] = {'nouveau': make_serializable(val)}
             except:
                 pass
    else:
        # Update
        old_state = getattr(instance, '_old_state', {})
        new_state = model_to_dict(instance)
        
        # Check for diffs
        # We iterate over new_state because it represents the current fields interesting for the model
        for key, val in new_state.items():
            old_val = old_state.get(key)
            if old_val != val:
                 champs_modifies[key] = {
                     'ancien': make_serializable(old_val), 
                     'nouveau': make_serializable(val)
                 }

    if not champs_modifies and not created:
        return

    if not champs_modifies and not created:
        return

    # Get User from Thread Local (set by ViewSet)
    from .middleware import get_thread_user
    app_user = get_thread_user()

    # Fallback to request user if thread user not set (e.g. Admin panel)
    if not app_user:
        try:
             from .middleware import get_current_request
             request = get_current_request()
             if request and request.user and request.user.is_authenticated:
                  if hasattr(request.user, 'utilisateur'):
                      app_user = request.user.utilisateur
                  elif hasattr(request.user, 'username'):
                      app_user = Utilisateur.objects.filter(nomUtilisateur=request.user.username).first()
        except:
             pass

    try:
        Log.objects.create(
            type=action,
            nomTable=sender._meta.db_table or sender._meta.model_name,
            idCible={'id': instance.pk},
            champsModifies=champs_modifies,
            utilisateur=app_user
        )
    except Exception as e:
        print(f"Error creating log: {e}")

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender._meta.model_name in ['log', 'session', 'contenttype', 'migration', 'adminlog']:
        return

    django_user = get_current_user()
    app_user = None
    if django_user and django_user.is_authenticated:
        if hasattr(django_user, 'utilisateur'):
            app_user = django_user.utilisateur
        elif hasattr(django_user, 'username'):
             app_user = Utilisateur.objects.filter(nomUtilisateur=django_user.username).first()

    try:
        Log.objects.create(
            type='suppression',
            nomTable=sender._meta.db_table or sender._meta.model_name,
            idCible={'id': instance.pk},
            champsModifies={'deleted': True},
            utilisateur=app_user
        )
    except Exception as e:
        print(f"Error creating log: {e}")
