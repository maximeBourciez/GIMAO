<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Détails d’un équipement
    </div>

    <div class="text-body-2 mb-4">
      En cliquant sur un équipement, vous accédez à sa fiche détaillée.
      <br /><br />
      Vous pouvez y consulter :
      <br />
      • Sa désignation<br />
      • Sa référence<br />
      • Sa localisation<br />
      • Son état<br />
      • Les documents associés
    </div>

    <ZoomImage src="/images/equipement-detail.png" alt="Détail équipement" />
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>