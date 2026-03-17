<template>
  <div class="doc-page">
    <div class="text-body-1 font-weight-bold mb-2">
      Tableau de bord
    </div>

    <div class="text-body-2 mb-4">
      Après la connexion, votre tableau de bord s’affiche automatiquement.
      Il centralise les informations essentielles liées à votre activité.
      <br /><br />

      En haut de l’écran, vous trouverez plusieurs indicateurs :
      <br /><br />

      • <strong>Vos DI</strong> : nombre total de Demandes d’Intervention que vous avez créées.<br />
      • <strong>Vos DI en attente</strong> : demandes qui n’ont pas encore été traitées par le Responsable GMAO.<br />
      • <strong>Vos DI acceptées</strong> : demandes validées et en attente d’un diagnostic ou d’une prise en charge.<br /><br />

      Le tableau de bord donne également accès à des accès rapides vers les principales fonctionnalités :
      <br /><br />

      • Un panneau dédié à vos Demandes d’Intervention, détaillé dans la section
      <em>Demande d’Intervention &gt; Consulter vos DI</em>.<br />

      • Une liste des équipements de l’entreprise, décrite dans la section
      <em>Équipements &gt; Liste des équipements</em>.<br /><br />

      Le contenu affiché dépend des droits attribués à votre compte.
    </div>

    <ZoomImage src="/images/dashboard.png" alt="Tableau de bord" />
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>

<style scoped>
.doc-page {
  max-width: 80%;
  margin: auto;
  margin-bottom: 2rem;
}
</style>