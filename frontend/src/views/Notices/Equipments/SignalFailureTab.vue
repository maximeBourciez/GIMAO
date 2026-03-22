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

    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-creer-di-operateur.png')" alt="Signalement depuis détail équipement" v-if="role === 'Opérateur'"/>
    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-creer-di-technicien.png')" alt="Signalement depuis détail équipement" v-else/>
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";

const props = defineProps({
  role: {
    type: String,
    default: "Opérateur"
  }
});

const roles = ["Opérateur", "Technicien", "Responsable GMAO"];

const roleIsAbove = (minRole) => {
  return roles.indexOf(props.role) >= roles.indexOf(minRole);
};
</script>