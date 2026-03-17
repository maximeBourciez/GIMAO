<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Équipements
    </div>

    <div class="text-body-2 mb-4">
      Vous pouvez consulter les équipements disponibles dans l’application.
      <br /><br />
      • Accédez à la liste des équipements<br />
      • Cliquez sur un équipement pour voir ses détails<br />
      • Consultez ses informations et son état<br /><br />
      Depuis un équipement, vous pouvez également signaler une défaillance.
    </div>

    <ZoomImage src="/images/equipements.png" alt="Liste équipements" />
    <ZoomImage src="/images/equipement-detail.png" alt="Détail équipement" />
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>