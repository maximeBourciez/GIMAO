<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Signaler une défaillance
    </div>

    <div class="text-body-2 mb-4">
      Depuis la fiche d'un équipement, vous pouvez déclarer une nouvelle défaillance. En cliquant sur le bouton «
      Signaler une défaillance », vous serez redirigé vers le formulaire de création d'une Demande d'Intervention (DI).
      Le fonctionnement de ce formulaire est détaillé dans la section Demande d'Intervention > Création d'une DI.
    </div>

    <ZoomImage :src="require('@/assets/images/notices/equips/creer-di.png')" alt="Signalement depuis détail équipement"/>
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>