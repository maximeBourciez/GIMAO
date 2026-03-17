<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Tableau de bord
    </div>

    <div class="text-body-2 mb-4">
      Après la connexion, votre tableau de bord s’affiche automatiquement.
      Il centralise les informations utiles à votre activité :
      <br /><br />
      • Des indicateurs et statistiques visibles en haut de l’écran<br />
      • L’accès rapide à vos demandes d’intervention<br />
      • Les actions principales disponibles pour votre rôle<br /><br />
      Le contenu dépend des droits accordés à votre compte.
    </div>

    <ZoomImage src="/images/dashboard.png" alt="Tableau de bord" />
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>