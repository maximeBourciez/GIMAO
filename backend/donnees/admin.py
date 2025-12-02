from django.contrib import admin

from .models import *

admin.site.register(Document)
admin.site.register(TypeDocument)
admin.site.register(Lieu)
admin.site.register(Fabricant)
admin.site.register(Fournisseur)
admin.site.register(Adresse)