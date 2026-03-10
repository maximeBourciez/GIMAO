<template>
  <div class="py-2">
    <div class="text-body-2 mb-4">
      En tant que responsable GMAO, vous avez un accès complet à l'application : traitement des DI (demandes d'intervention), gestion des BT (bons de travail), des équipements, des stocks, des utilisateurs et des données de référence.
    </div>

    <!-- Tableau de bord -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">1) Votre tableau de bord</div>
    <div class="text-body-2">
      - Votre tableau de bord présente côte à côte :<br />
      &nbsp;&nbsp;• <strong>Les DI</strong> en cours, avec possibilité d'en créer une nouvelle.<br />
      &nbsp;&nbsp;• <strong>Les BT</strong> en cours, avec possibilité d'en créer un nouveau.<br />
      - Des statistiques complètes (DI, BT, équipements) sont affichées en haut de la page.
    </div>

    <!-- Demandes d'intervention -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">2) DI (demandes d'intervention)</div>
    <div class="text-body-2">
      - <strong>Consulter</strong> : accédez à la liste complète des demandes et au détail de chacune.<br />
      - <strong>Créer</strong> : signalez un problème (nom, équipement, commentaire, documents).<br />
      - <strong>Accepter</strong> : validez la pertinence de la demande (état → <em>Acceptée</em>).<br />
      - <strong>Refuser</strong> : rejetez une demande non pertinente (état → <em>Refusée</em>).<br />
      - <strong>Transformer en bon de travail</strong> : convertissez une demande acceptée pour planifier l'intervention (état → <em>Transformée</em>).<br />
      - <strong>Modifier / Supprimer / Exporter</strong> : contrôle total sur toutes les demandes.
    </div>

    <!-- Bons de travail -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">3) BT (bons de travail)</div>
    <div class="text-body-2">
      - <strong>Créer</strong> : directement ou via la transformation d'une DI. Renseignez le diagnostic, le type (correctif/préventif), la date planifiée, et désignez un ou plusieurs techniciens.<br />
      - <strong>Cycle de vie</strong> :<br />
      &nbsp;&nbsp;1. <em>En attente</em> : créé, en attente d'exécution.<br />
      &nbsp;&nbsp;2. <em>En cours</em> : le technicien a démarré.<br />
      &nbsp;&nbsp;3. <em>Terminé</em> : le technicien a fini.<br />
      &nbsp;&nbsp;4. <em>Clôturé</em> : vous validez la clôture après vérification.<br />
      - <strong>Accepter la clôture</strong> : clôturez définitivement le BT après vérification.<br />
      - <strong>Refuser la clôture</strong> : renvoyez le BT au technicien avec un commentaire.<br />
      - <strong>Valider les consommables</strong> : approuvez les demandes de consommables des techniciens.<br />
      - <strong>Modifier / Supprimer / Exporter</strong> : contrôle total sur tous les BT.
    </div>

    <!-- Équipements -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">4) Équipements</div>
    <div class="text-body-2">
      - <strong>Créer</strong> : renseignez la désignation, la référence, le numéro de série, la localisation, le fabricant, le fournisseur, le modèle, la famille, et joignez des documents.<br />
      - <strong>Modifier / Supprimer</strong> un équipement existant.<br />
      - <strong>Gérer les compteurs</strong> : créez des compteurs (heures, km, cycles…) et configurez des seuils de déclenchement pour la maintenance préventive.<br />
      - <strong>Plans de maintenance</strong> : associez des plans aux seuils des compteurs (consommables nécessaires, documents, habilitations requises).<br />
      - <strong>Exporter</strong> les données équipements.
    </div>

    <!-- Maintenance préventive -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">5) Maintenance préventive</div>
    <div class="text-body-2">
      - Configurez des seuils sur les compteurs d'un équipement.<br />
      - Chaque seuil est lié à un plan de maintenance définissant les consommables, les documents de référence et les habilitations requises (électrique, permis feu).<br />
      - Lorsqu'un compteur atteint son seuil, un BT préventif est automatiquement généré.<br />
      - Le mode <strong>glissant</strong> recalcule le prochain seuil à partir de la dernière intervention.
    </div>

    <!-- Stocks -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">6) Stocks</div>
    <div class="text-body-2">
      - Consultez et gérez les consommables, les entrepôts et les niveaux de stock.<br />
      - Vous avez les mêmes droits que le magasinier sur la gestion des stocks.
    </div>

    <!-- Utilisateurs -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">7) Gestion des utilisateurs</div>
    <div class="text-body-2">
      - <strong>Créer</strong> un compte : renseignez l'identifiant, le nom, le prénom, l'adresse électronique, la photo et attribuez un rôle.<br />
      - <strong>Modifier</strong> les informations ou le rôle d'un utilisateur.<br />
      - <strong>Désactiver / Réactiver</strong> un compte sans le supprimer.<br />
      - <strong>Supprimer</strong> un compte définitivement.<br />
      - <strong>Réinitialiser le mot de passe</strong> d'un utilisateur en cas d'oubli.
    </div>

    <!-- Données de référence -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">8) Données de référence</div>
    <div class="text-body-2">
      - Accessible via le menu <strong>Gestion des données</strong>, cette rubrique regroupe :<br />
      &nbsp;&nbsp;• <strong>Lieux</strong> : structure hiérarchique des emplacements (bâtiments, étages, zones…).<br />
      &nbsp;&nbsp;• <strong>Fournisseurs</strong> : coordonnées, service après-vente, adresse.<br />
      &nbsp;&nbsp;• <strong>Fabricants</strong> : coordonnées, service après-vente, adresse.<br />
      &nbsp;&nbsp;• <strong>Modèles d'équipements</strong> : modèles liés à un fabricant.<br />
      - Pour chaque catégorie, vous pouvez créer, modifier, supprimer et exporter les données.
    </div>
  </div>
</template>
