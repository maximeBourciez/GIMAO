<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Détails d’un équipement
    </div>

    <div class="text-body-2 mb-4">
      Lorsque vous cliquez sur un équipement, vous accédez à sa page de détails. Cette page vous présente une vue
      d’ensemble des informations disponibles concernant l’équipement. Vous pouvez y consulter ses caractéristiques
      ainsi que les documents associés, si ceux-ci ont été renseignés par vos supérieurs. Ces documents peuvent
      notamment contenir des notices ou des manuels d’utilisation utiles.
    </div>

    <ZoomImage src="/images/equipement-detail.png" alt="Détail équipement" />

    <div class="text-body-2 mb-4">
      En bas à gauche de la page, vous pouvez trouver les dits documents associés à l’équipement. Cliquez sur un
      document pour l’ouvrir et le consulter.
    </div>

    <div class="text-body-2 mb-4">
      Depuis cette page, vous pouvez également signaler une défaillance en cliquant sur le bouton <strong>Créer
        une DI</strong>. Le formulaire de création de DI s’ouvre alors avec l’équipement déjà sélectionné, ce qui
      facilite le signalement.
    </div>
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>