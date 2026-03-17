<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Liste des équipements
    </div>

    <div class="text-body-2 mb-4">
      La liste des équipements vous permet de consulter l’ensemble des équipements de votre entreprise. Elle donne accès
      aux informations détaillées de chaque équipement et peut également servir à signaler une défaillance directement
      depuis celui-ci.

      Si vous devez modifier l’état d’un équipement, cette action s’effectue via la création d’une Demande
      d’Intervention (DI). Lors du signalement, vous pourrez sélectionner le nouvel état correspondant à la situation.
    </div>

    <ZoomImage src="/images/equipements-list.png" alt="Liste des équipements" />
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>