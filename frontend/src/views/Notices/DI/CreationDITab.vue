<template>
  <v-container class="doc-page">
    <h4>Créer une DI</h4>

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
      :src="require('@/assets/images/notices/DI/formulaire-di.png')"
      alt="Formulaire DI"
    />

    <p>
      Les différents champs du formulaire ont la signification suivante :<br />
      <strong>Nom</strong> : description synthétique de la panne ou du problème constaté.<br />
      <strong>Équipement</strong> : équipement concerné par la défaillance.<br />
      <strong>Statut supposé</strong> : nouvel état proposé pour l’équipement à la suite du signalement.<br />
      <strong>Commentaires</strong> : espace permettant d’apporter des précisions sur l’incident, par exemple les circonstances ou les éléments observés.<br />
      <strong>Documents</strong> : possibilité d’ajouter des fichiers (par exemple des photos). Veillez à sélectionner le type de document approprié et à lui attribuer un nom explicite.
    </p>

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