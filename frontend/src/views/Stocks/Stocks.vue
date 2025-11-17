<template>
    <v-app>
      <v-main>
        <v-container>
          <v-row>
            <v-col>
              <v-data-table
                :headers="headers"
                :items="consommables"
                :items-per-page="5"
                class="elevation-1 rounded-lg"
              ></v-data-table>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    name: 'Consommables',
    data() {
      return {
        headers: [
          { text: 'Nom', value: 'nom' },
          { text: 'Quantité', value: 'quantite' },
          { text: 'Prix unitaire', value: 'prixUnitaire' },
          { text: 'Date d\'achat', value: 'dateAchat' },
        ],
        consommables: [
          { nom: 'Vis à bois - modèle : tête fraisée', quantite: 20, prixUnitaire: 'France', dateAchat: 'leroymerlin@gmail.com' },
          { nom: 'Chevilles - modèle plastique', quantite: 145, prixUnitaire: 'Mexique', dateAchat: 'castorama@gmail.com' },
          { nom: 'Clous - modèle : tête plate', quantite: 60, prixUnitaire: 'Corée du Nord', dateAchat: 'Demande d\'intervention' },
          { nom: 'Bandes adhésive', quantite: 80, prixUnitaire: 'Corée du Sud', dateAchat: 'Bon de travail' },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .v-card {
    background-color: #FFFFFF;
  }
  </style>
  