<template>
  <v-container class="doc-page">

    <p>
      Si vous souhaitez signaler une nouvelle défaillance sur un équipement,
      vous pouvez le faire directement depuis le tableau de bord.
      En effet, vous disposez d'un bouton <strong>"Créer une DI"</strong>
      qui permet le signalement de la défaillance.
    </p>

    <ZoomImage
      :src="require('@/assets/images/notices/DI/creer-di.png')"
      alt="Bouton créer DI"
    />

    <p>
      En cliquant dessus, vous serez redirigé vers un formulaire à remplir
      afin que vous puissiez fournir toutes les informations en votre
      possession au Responsable de la maintenance.
    </p>

    <ZoomImage
      src="require('@/assets/images/notices/DI/formulaire-di.png')"
      alt="Formulaire DI"
    />

    <p>
      Pour lui donner ces informations, il vous suffit de remplir les champs
      demandés, puis de cliquer sur <strong>"Valider"</strong>.
    </p>

  </v-container>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>

<style scoped>
.doc-page {
  max-width: 900px;
  margin: auto;
  line-height: 1.6;
}

p {
  margin-bottom: 20px;
}
</style>