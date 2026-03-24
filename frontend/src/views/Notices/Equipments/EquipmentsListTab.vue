<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Liste des équipements
    </div>

    <div class="text-body-2 mb-4">
      La liste des équipements est consultable dans le menu correspondant ainsi que dans votre tableau de bord. 
      Elle vous permet de consulter l'ensemble des équipements de votre entreprise. Elle donne accès
      aux informations détaillées de chaque équipement et peut également servir à signaler une défaillance directement
      depuis celui-ci.

      Si vous devez modifier l'état d'un équipement, cette action s'effectue via la création d'une Demande
      d'Intervention (DI). Lors du signalement, vous pourrez sélectionner le nouvel état correspondant à la situation.
    </div>

    <ZoomImage :src="require('@/assets/images/notices/equips/list-eq-operateur.png')" alt="Liste des équipements" v-if="props.role === 'Opérateur'" />
    <ZoomImage :src="require('@/assets/images/notices/equips/list-eq-technicien.png')" alt="Liste des équipements" v-if="roleIsAbove('Technicien')" />
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