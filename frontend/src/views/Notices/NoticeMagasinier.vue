<template>
  <div class="py-2">
    <div class="text-body-2 mb-4">
      En tant que magasinier, vous gérez les stocks de consommables et les entrepôts, et vous validez les demandes de consommables associées aux BT (bons de travail).
    </div>

    <!-- Tableau de bord -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">1) Votre tableau de bord</div>
    <div class="text-body-2">
      - Votre tableau de bord affiche directement la gestion des stocks et des entrepôts.<br />
      - Vous y retrouvez un aperçu rapide des niveaux de stock.
    </div>

    <!-- Consommables -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">2) Gestion des consommables</div>
    <div class="text-body-2">
      - Depuis la page <strong>Stocks</strong>, consultez la liste de tous les consommables.<br />
      - <strong>Créer un consommable</strong> : remplissez la fiche (désignation, image, seuil d'alerte, fournisseurs, compatibilité avec des modèles d'équipements).<br />
      - <strong>Modifier</strong> : mettez à jour les informations, les prix fournisseurs ou les documents associés.<br />
      - <strong>Supprimer</strong> un consommable devenu obsolète.<br />
      - Surveillez les niveaux : les consommables sous le <strong>seuil d'alerte</strong> sont mis en évidence pour anticiper les réapprovisionnements.
    </div>

    <!-- Entrepôts -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">3) Gestion des entrepôts</div>
    <div class="text-body-2">
      - Un entrepôt est un lieu de stockage physique (fixe ou mobile).<br />
      - <strong>Créer un entrepôt</strong> : renseignez son nom, son type (fixe/mobile) et son adresse.<br />
      - <strong>Modifier / Supprimer</strong> un entrepôt existant.<br />
      - Chaque entrepôt affiche les quantités de consommables qu'il contient.
    </div>

    <!-- Niveaux de stock -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">4) Suivi des niveaux de stock</div>
    <div class="text-body-2">
      - Pour chaque consommable, consultez la quantité disponible par entrepôt.<br />
      - Vous pouvez <strong>exporter</strong> les données de stock pour un suivi externe.
    </div>

    <!-- Demandes de consommables -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">5) Valider les demandes de consommables</div>
    <div class="text-body-2">
      - Lorsqu'un technicien demande des consommables dans un BT, vous recevez la demande.<br />
      - Depuis le détail du BT, cliquez sur <strong>Accepter</strong> pour valider la demande.<br />
      - Le stock de l'entrepôt concerné est automatiquement mis à jour.<br />
      - Accédez à la liste complète des BT pour consulter les demandes en attente.
    </div>

    <!-- Bons de travail -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">6) Consulter les BT</div>
    <div class="text-body-2">
      - Vous avez accès en lecture à tous les BT (bons de travail).<br />
      - Cela vous permet de voir quels consommables ont été demandés ou utilisés pour chaque intervention.
    </div>
  </div>
</template>
