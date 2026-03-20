<template>
  <v-container class="doc-page">
    <h4>Consulter la liste des stocks</h4>

    <div class="text-body-2 mb-4 mt-2">
      La rubrique <strong>Stocks</strong> offre une vue globale sur l'ensemble des pièces détachées et consommables de l'entreprise. Cette liste vous permet d'anticiper vos besoins ou de vérifier les disponibilités.
      <br /><br />

      <strong>Informations disponibles dans la liste :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Désignation :</strong> le nom et la référence interne des différentes pièces.</li>
        <li><strong>Quantité disponible :</strong> le niveau actuel des stocks physiques, vous indiquant en temps réel s'il y a assez de matériel pour mener à bien de futures interventions.</li>
        <li><strong>Informations complémentaires :</strong> données générales sur le prix unitaire ou la valeur globale des éléments.</li>
      </ul>

      <strong>Droits et permissions :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Consultation :</strong> vous pouvez à tout moment vérifier la présence d'une pièce et son niveau de stock en lisant simplement cette liste.</li>
        <li v-if="!roleIsAbove('Magasinier')"><strong>Modification :</strong> en tant que technicien, toute modification manuelle des quantités du stock vous est impossible depuis cet onglet. L'entrée de nouvelles quantités en stock ou l'ajustement manuel ne peuvent être effectués que par le Magasinier ou le Responsable. Le technicien n'influence le stock que par l'utilisation de la fonctionnalité "Demande de consommables" dans une intervention.</li>
        <li v-else><strong>Modification :</strong> en tant que Magasinier ou Responsable, vous avez les permissions nécessaires pour ajouter manuellement des pièces ou ajuster les niveaux d'un produit (entrée, sortie, erreur d'inventaire).</li>
      </ul>
    </div>

    <ZoomImage :src="require('@/assets/images/notices/stocks/liste-technicien-stock.png')" alt="Liste des stocks" v-if="role === 'Technicien'"/>
  </v-container>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";

const props = defineProps({
  role: {
    type: String,
    default: "Technicien"
  }
});

const roles = ["Opérateur", "Technicien", "Magasinier", "Responsable GMAO"];

const roleIsAbove = (minRole) => {
  return roles.indexOf(props.role) >= roles.indexOf(minRole);
};
</script>

<style scoped>
.doc-page {
  padding: 0;
}
ul li {
  margin-bottom: 8px;
}
</style>
