<template>
  <v-container class="doc-page">
    <h4>Détails et traçabilité d'un consommable</h4>

    <div class="text-body-2 mb-4 mt-2">
      En cliquant sur une pièce spécifique depuis la liste des stocks, vous accédez à sa <strong>fiche détaillée</strong>. Cette fiche centralise toutes les opérations effectuées sur ce produit, assurant ainsi une traçabilité complète de son utilisation dans l'entreprise.
      <br /><br />

      <strong>Contenu de la fiche d'un consommable :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Informations générales :</strong> la référence exacte de l'article, sa description détaillée, ainsi que sa valorisation financière.</li>
        <li><strong>État et répartition du stock :</strong> au-delà de la quantité physiquement disponible, vous pouvez y apercevoir les pièces en cours de réapprovisionnement, ou encore celles qui sont "réservées" par des techniciens pour des Bons de Travail à venir.</li>
      </ul>

    </div>
  </v-container>
</template>

<script setup>
</script>

<style scoped>
.doc-page {
  padding: 0;
}
ul li {
  margin-bottom: 8px;
}
</style>
