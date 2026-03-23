<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Détails d'un équipement
    </div>

    <div class="text-body-2 mb-4">
      Lorsque vous cliquez sur un équipement, vous accédez à sa page de détails. Cette page vous présente une vue
      d'ensemble des informations disponibles concernant l'équipement. Vous pouvez y consulter ses caractéristiques
      ainsi que les documents associés, si ceux-ci ont été renseignés par vos supérieurs. Ces documents peuvent
      notamment contenir des notices ou des manuels d'utilisation utiles.
    </div>

    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-operateur.png')" alt="Détail équipement" v-if="props.role === 'Opérateur'"/>
    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-technicien.png')" alt="Détail équipement" v-else/>

    <div class="text-body-1 font-weight-bold mb-2">
      En bas de la colonne gauche, vous pourrez trouver les dits documents associés à l'équipement, s'ils ont été renseignés par vos supérieurs.
    </div>

    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-docs-operateur.png')" alt="Détail équipement" v-if="role === 'Opérateur'"/>
    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-docs-technicien.png')" alt="Détail équipement" v-else/>

    <div class="text-body-2 mb-4">
      Depuis cette page, vous pouvez également signaler une défaillance en cliquant sur le bouton <strong>Créer
        une DI</strong>. Le formulaire de création de DI s'ouvre alors avec l'équipement déjà sélectionné, ce qui
      facilite le signalement.
    </div>

    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-creer-di-operateur.png')" alt="Signalement depuis détail équipement" v-if="role === 'Opérateur'"/>
    <ZoomImage :src="require('@/assets/images/notices/equips/detail-eq-creer-di-technicien.png')" alt="Signalement depuis détail équipement" v-else/>

    <div v-if="roleIsAbove('Technicien')" class="mt-4">
      <div class="text-body-1 font-weight-bold mb-2">
        Modification et compteurs
      </div>
      <div class="text-body-2 mb-4">
        <!-- - Vous pouvez <strong>modifier</strong> un équipement : mettre à jour son état, sa localisation, ses informations.<br /> -->
        - Vous avez accès aux <strong>compteurs</strong> de chaque équipement : consultez et modifiez les valeurs (heures, km, cycles…).
      </div>
    </div>
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