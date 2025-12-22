from django.db import models

class Lieu(models.Model):
    nomLieu = models.CharField(max_length=50, help_text="Nom du lieu.")
    typeLieu = models.CharField(
        max_length=50,
        help_text="Informations complémentaires optionnelles sur le type de lieu renseigné."
    )
    lienPlan = models.CharField(max_length=200, blank=True, null=True, help_text="Lien vers un plan du lieu.")
    lieuParent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Pointeur désignant la structure (un autre lieu) où se trouve l'élément en question."
    )
    x = models.FloatField(null=True, blank=True, help_text="Coordonnée X du lieu par rapport à son lieu parent.")
    y = models.FloatField(null=True, blank=True, help_text="Coordonnée Y du lieu par rapport à son lieu parent.")

    def __str__(self):
        return self.nomLieu

    class Meta:
        db_table = 'gimao_lieu'
        verbose_name = 'Lieu'
        verbose_name_plural = 'Lieux'
        


class TypeDocument(models.Model):
    nomTypeDocument = models.CharField(max_length=50)

    def __str__(self):
        return self.nomTypeDocument

    class Meta:
        db_table = 'gimao_type_document'
        verbose_name = 'Type de document'
        verbose_name_plural = 'Types de document'

class Document(models.Model):
    nomDocument = models.CharField(max_length=100, help_text="Nom du document.")
    cheminAcces = models.FileField(upload_to='documents/', help_text="Chemin d'accès au fichier du document.")
    typeDocument = models.ForeignKey(
        TypeDocument,
        on_delete=models.CASCADE,
        help_text="Type du document."
    )

    def __str__(self):
        return self.nomDocument

    class Meta:
        db_table = 'gimao_document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        
        
class Fabricant(models.Model):
    """
    Représente un fabricant d'équipements.
    """
    nom = models.CharField(max_length=100, help_text="Nom du fabricant")
    email = models.EmailField(max_length=191, blank=True, null=True, help_text="Adresse email du fabricant")
    numTelephone = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone du fabricant")
    serviceApresVente = models.BooleanField(default=False, help_text="Indique si le fabricant propose un service après-vente")
    adresse = models.ForeignKey('Adresse', on_delete=models.CASCADE, null=True, blank=True, help_text="Adresse du fabricant")

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'gimao_fabricant'
        verbose_name = 'Fabricant'
        verbose_name_plural = 'Fabricants'
        


class Fournisseur(models.Model):
    """
    Représente un fournisseur d'équipements.
    """
    nom = models.CharField(max_length=100, help_text="Nom du fournisseur")
    email = models.EmailField(max_length=191, blank=True, null=True, help_text="Adresse email du fournisseur")
    numTelephone = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone du fournisseur")
    serviceApresVente = models.BooleanField(default=False, help_text="Indique si le fournisseur propose un service après-vente")
    adresse = models.ForeignKey('Adresse', on_delete=models.CASCADE, null=True, blank=True, help_text="Adresse du fournisseur")

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'gimao_fournisseur'
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'   


class Adresse(models.Model):
    """
    Représente une adresse physique.
    """
    numero = models.CharField(max_length=10, help_text="Numéro de l'adresse")
    rue = models.CharField(max_length=255, help_text="Nom de la rue")
    ville = models.CharField(max_length=100, help_text="Nom de la ville")
    code_postal = models.CharField(max_length=20, help_text="Code postal")
    pays = models.CharField(max_length=100, help_text="Nom du pays")
    complement = models.CharField(max_length=255, blank=True, null=True, help_text="Complément d'adresse optionnel")
    
    def __str__(self):
        return f"{self.rue}, {self.ville}, {self.code_postal}, {self.pays}"
    
    class Meta:
        db_table = 'gimao_adresse'
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'