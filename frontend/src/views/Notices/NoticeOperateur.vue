<template>
  <div class="py-2">
    <div class="text-body-2 mb-4">
      En tant qu'opérateur, votre rôle principal est de signaler les pannes constatées sur les équipements et d'en suivre le traitement. Vous n'avez pas accès aux stocks ni à la gestion des comptes.
    </div>

    <!-- Tableau de bord -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">1) Votre tableau de bord</div>
    <div class="text-body-2">
      - À la connexion, votre tableau de bord affiche :<br />
      &nbsp;&nbsp;• <strong>Vos demandes d'intervention</strong> : celles que vous avez créées, avec leur état actuel.<br />
      &nbsp;&nbsp;• <strong>Liste des équipements</strong> du parc que vous pouvez consulter.<br />
      - Des statistiques sur vos demandes sont affichées en haut de page.
    </div>

    <!-- Signaler une panne -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">2) Signaler une panne (créer une DI)</div>
    <div class="text-body-2">
      - Depuis votre tableau de bord, cliquez sur <strong>Créer une DI</strong> (ou depuis la fiche d'un équipement).<br />
      - Remplissez le formulaire :<br />
      &nbsp;&nbsp;• <strong>Nom</strong> : un titre court décrivant le problème.<br />
      &nbsp;&nbsp;• <strong>Équipement</strong> : sélectionnez l'équipement concerné.<br />
      &nbsp;&nbsp;• <strong>Commentaire</strong> : décrivez le problème constaté le plus précisément possible.<br />
      - Vous pouvez joindre des documents (photos, etc.) pour illustrer la panne.<br />
      - Validez : la DI est créée avec l'état <strong>En attente</strong>.
    </div>

    <!-- Suivi -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">3) Suivre vos DI</div>
    <div class="text-body-2">
      - Vos DI apparaissent sur votre tableau de bord avec leur état :<br />
      &nbsp;&nbsp;• <strong>En attente</strong> : la demande n'a pas encore été traitée.<br />
      &nbsp;&nbsp;• <strong>Acceptée</strong> : le responsable a validé la demande.<br />
      &nbsp;&nbsp;• <strong>Transformée</strong> : la DI a été convertie en BT, une intervention est planifiée.<br />
      &nbsp;&nbsp;• <strong>Refusée</strong> : le responsable a jugé la demande non pertinente.<br />
      - Cliquez sur une demande pour voir son détail complet.
    </div>

    <!-- Modifier -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">4) Modifier une DI</div>
    <div class="text-body-2">
      - Vous pouvez modifier une demande que <strong>vous avez créée</strong>, tant qu'elle est encore en attente ou acceptée.<br />
      - Depuis le détail de la demande, cliquez sur <strong>Modifier</strong> pour changer le nom, le commentaire ou les documents.
    </div>

    <!-- Équipements -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">5) Consulter les équipements</div>
    <div class="text-body-2">
      - La liste des équipements est accessible depuis votre tableau de bord.<br />
      - Cliquez sur un équipement pour voir sa fiche : désignation, référence, localisation, état, documents associés.<br />
      - Depuis la fiche d'un équipement, vous pouvez directement <strong>créer une DI</strong> pré-remplie.
    </div>

    <!-- Bons de travail -->
    <div class="text-body-1 font-weight-bold mt-4 mb-1">6) Consulter les BT</div>
    <div class="text-body-2">
      - Vous avez accès en lecture seule à la liste des BT (bons de travail).<br />
      - Cela vous permet de suivre l'avancement des interventions liées à vos DI.
    </div>
  </div>
</template>
