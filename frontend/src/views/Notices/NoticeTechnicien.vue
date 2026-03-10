<template>
  <div class="py-2">
    <div class="text-body-2 mb-4">
      En tant que technicien, vous réalisez les interventions sur les équipements. Vous pouvez signaler des pannes, gérer vos bons de travail et consulter les équipements et les stocks.
    </div>

    <!-- Tableau de bord -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">1) Votre tableau de bord</div>
    <div class="text-body-2">
      - Votre tableau de bord affiche :<br />
      &nbsp;&nbsp;• <strong>Liste des équipements</strong> du parc.<br />
      &nbsp;&nbsp;• <strong>Vos BT</strong> : ceux qui vous ont été confiés.<br />
      - Des statistiques sur les bons de travail (en cours, terminés, en retard) sont affichées en haut.
    </div>

    <!-- Menu -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">2) Menu de navigation</div>
    <div class="text-body-2">
      - Vous disposez d'un <strong>menu latéral</strong> avec les rubriques :<br />
      &nbsp;&nbsp;• <strong>Tableau de bord</strong><br />
      &nbsp;&nbsp;• <strong>Équipements</strong> : consulter et modifier les fiches équipements.<br />
      &nbsp;&nbsp;• <strong>Demandes d'intervention (DI)</strong> : consulter et créer des DI.<br />
      &nbsp;&nbsp;• <strong>Bons de travail (BT)</strong> : consulter et réaliser les interventions.<br />
      &nbsp;&nbsp;• <strong>Stocks</strong> : consulter les niveaux de stock (lecture seule).
    </div>

    <!-- Équipements -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">3) Équipements</div>
    <div class="text-body-2">
      - Consultez la liste complète des équipements et cliquez sur l'un d'eux pour voir sa fiche.<br />
      - Vous pouvez <strong>modifier</strong> un équipement : mettre à jour son état, sa localisation, ses informations.<br />
      - Vous avez accès aux <strong>compteurs</strong> de chaque équipement : consultez et modifiez les valeurs (heures, km, cycles…).<br />
      - Depuis la fiche d'un équipement, vous pouvez rapidement créer une DI.
    </div>

    <!-- Demandes d'intervention -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">4) Demandes d'intervention (DI)</div>
    <div class="text-body-2">
      - Vous pouvez <strong>créer</strong> une DI pour signaler un problème constaté sur un équipement.<br />
      - Vous pouvez <strong>modifier</strong> les DI que vous avez créées (tant qu'elles ne sont pas transformées).<br />
      - Consultez le détail de toutes les DI pour suivre leur état.
    </div>

    <!-- Bons de travail -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">5) Bons de travail (BT)</div>
    <div class="text-body-2">
      - Les BT qui vous sont confiés apparaissent sur votre tableau de bord et dans la rubrique <strong>Bons de travail</strong>.<br />
      - <strong>Démarrer une intervention</strong> : depuis le détail d'un BT qui vous est confié, cliquez sur <strong>Démarrer</strong>. L'état passe à <em>En cours</em> et la date de début est enregistrée.<br />
      - <strong>Terminer une intervention</strong> : une fois le travail achevé, cliquez sur <strong>Terminer</strong>. L'état passe à <em>Terminé</em> et la date de fin est enregistrée.<br />
      - Vous pouvez <strong>modifier</strong> les BT qui vous sont confiés (diagnostic, commentaire, documents).<br />
      - Vous pouvez <strong>joindre des documents</strong> (rapport d'intervention, photos, etc.).
    </div>

    <!-- Consommables -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">6) Demander des consommables</div>
    <div class="text-body-2">
      - Lors de la modification d'un BT, vous pouvez indiquer les consommables nécessaires à l'intervention.<br />
      - La demande sera validée par le magasinier ou le responsable avant que le stock soit mis à jour.
    </div>

    <!-- Maintenance préventive -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">7) Plans de maintenance</div>
    <div class="text-body-2">
      - Vous pouvez consulter les plans de maintenance liés aux compteurs d'un équipement.<br />
      - Un BT préventif est automatiquement généré lorsqu'un compteur atteint un seuil défini.<br />
      - Ces BT préventifs vous sont confiés de la même façon que les BT correctifs.
    </div>

    <!-- Stocks -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">8) Consulter les stocks</div>
    <div class="text-body-2">
      - La rubrique <strong>Stocks</strong> vous permet de vérifier la disponibilité d'un consommable avant d'en faire la demande.<br />
      - La modification des stocks est réservée au magasinier.
    </div>
  </div>
</template>
