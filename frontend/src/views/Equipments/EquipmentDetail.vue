<template>
  <v-app>
    <v-main>
      <v-container v-if="!is_loading">
        <v-row>
          <!-- Section gauche : Détails de l'équipement -->
          <v-col cols="6">
            <v-card elevation="1" class="rounded-lg pa-2">
              <v-card-title class="font-weight-bold text-uppercase text-primary">Description de l'équipement</v-card-title>

              <v-row class="pa-2">
                <v-col cols="12" v-for="(value, key) in equipment_details" :key="key">
                  <p v-if="key !== 'statut'">
                    <strong>{{ format_label(key) }} :</strong> {{ format_value(value) }}
                  </p>
                  <p v-else>
                    <strong>{{ format_label(key) }} :</strong>
                    <v-chip
                      :color="get_status_color(value)"
                      text-color="white"
                      small
                    >
                      {{ value }}
                    </v-chip>
                  </p>
                </v-col>
              </v-row>

              <!-- Section documentation -->
                <v-card elevation="1" class="rounded-lg pa-2 mt-4">
                  <v-card-title class="font-weight-bold text-uppercase text-primary">Documentation</v-card-title>

                  <!-- Documents techniques -->
                  <v-card-subtitle class="pt-4">Documents techniques</v-card-subtitle>
                  <v-data-table
                    :headers="technical_documents_headers"
                    :items="equipement.liste_documents_techniques"
                    item-value="nomDocumentTechnique"
                    class="elevation-1 rounded-lg mb-4"
                    hide-default-footer
                  >
                    <template v-slot:item="{ item }">
                      <tr>
                        <td>{{ item.nomDocumentTechnique }}</td>
                        <td>
                          <v-btn
                            icon
                            small
                            color="primary"
                            center="center"
                            @click="download_document(item.lienDocumentTechnique, item.nomDocumentTechnique)"
                          >
                            <v-icon size="small">mdi-download</v-icon>
                          </v-btn>
                        </td>
                      </tr>
                    </template>
                  </v-data-table>

                  <!-- Autres documents -->
                  <v-card-subtitle class="pt-4">Autres documents</v-card-subtitle>
                  <v-data-table
                    :headers="others_documents_headers"
                    :items="others_documents"
                    class="elevation-1 rounded-lg"
                    hide-default-footer
                  >
                    <template v-slot:item="{ item }">
                      <tr>
                        <td>{{ item.type }}</td>
                        <td>{{ item.nomDocument }}</td>
                        <td>
                          <v-btn
                            icon
                            small
                            color="primary"
                            @click="download_document(item.lienDocument, item.nomDocument)"
                          >
                            <v-icon size="small">mdi-download</v-icon>
                          </v-btn>
                        </td>
                      </tr>
                    </template>
                  </v-data-table>
                </v-card>
            </v-card>
          </v-col>

          <!-- Section droite : Image, consommables, maintenance et actions -->
          <v-col cols="6">
            <!-- Section image -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-img
                :src="equipement.lienImageEquipement"
                aspect-ratio="4/3"
                class="rounded-lg"
                style="max-height: 30vh;"
                alt="Image de l'équipement"
              ></v-img>
            </v-card>

            <!-- Bouton d'action -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-actions class="justify-center">
                <!-- <v-btn color="primary" @click="edit_equipment">
                  Modifier l'équipement
                </v-btn> -->
                <v-btn color="warning" @click="signal_failure">
                  Signaler une défaillance
                </v-btn>
              </v-card-actions>
            </v-card>

            
            <!-- Section consommables -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">
                Consommables
              </v-card-title>
              <v-data-table
                :items="equipement.liste_consommables"
                :headers="consumable_headers"
                class="elevation-1 rounded-lg"
                hide-default-footer
              ></v-data-table>
            </v-card>

            <!-- Historique de maintenance -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">
                Interventions
              </v-card-title>
              <v-data-table
                :items="equipement.liste_interventions"
                :headers="interventions_headers"
                class="elevation-1 rounded-lg"
                hide-default-footer
              >
              <template v-slot:item.dateAssignation="{ item }">
                {{ format_date(item.dateAssignation) }}
              </template>
              <template v-slot:item.action="{ item }">
                <v-btn icon @click="view_intervention(item)">
                  <v-icon size="small">mdi-eye</v-icon>
                </v-btn>
              </template>
            </v-data-table>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <v-progress-circular
        v-else
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
    </v-main>
  </v-app>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { useApi } from '@/composables/useApi';
import { getStatusColor } from '@/utils/helpers';
import { API_BASE_URL, BASE_URL } from '@/utils/constants';


export default {
  name: 'EquipmentDetail',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const api = useApi(API_BASE_URL);
    const equipement = computed(() => api.data.value || {});
    const is_loading = computed(() => api.loading.value);
    
    const fetch_equipment_data = async () => {
      try {
        await api.get(`equipement/${route.params.reference}/affichage/`);
      } catch (error) {
        console.error("Erreur lors de la récupération des données de l'équipement:", error);
      }
    };
    
    onMounted(() => {
      fetch_equipment_data();
    });
    
    return { 
      router, 
      equipement, 
      is_loading,
      fetch_equipment_data 
    };
  },
  data() {
    
    return {
      technical_documents_headers: [
        { title: "Document technique", value: "nomDocumentTechnique", align: "start" },
        { title: "Télécharger", value: "action", align: "start", sortable: false }
      ],
      others_documents_headers: [
        { title: "Type", value: "type", align: "start" },
        { title: "Document", value: "nomDocument", align: "start" },
        { title: "Télécharger", value: "action", align: "start", sortable: false }
      ],
      consumable_headers: [
        { title: "Désignation", value: "designation" },
        { title: "Fabricant", value: "fabricant.nomFabricant" }
      ],
      interventions_headers: [
        { title: "Nom", value: "nomIntervention" },
        { title: "Date d'assignation", value: "dateAssignation" },
        { title: "Visualiser", value: "action", align: "start" }
      ]
    };
  },
  
  computed: {


    equipment_details() {
      if (!this.equipement) return {};
      const { 
        reference, designation, dateMiseEnService, prixAchat, 
        preventifGlissant, joursIntervalleMaintenance
      } = this.equipement;
      const lieu = this.equipement.lieu ? this.equipement.lieu.nomLieu : '';
      const modele = this.equipement.modeleEquipement ? this.equipement.modeleEquipement.nomModeleEquipement : '';
      const fournisseur = this.equipement.fournisseur ? this.equipement.fournisseur.nomFournisseur : '';
      const fabricant = this.equipement.fabricant ? this.equipement.fabricant.nomFabricant : '';
      const statut = this.equipement.dernier_statut ? this.equipement.dernier_statut.statutEquipement : '';
      
      return { 
        reference, designation, dateMiseEnService, prixAchat, 
        preventifGlissant, joursIntervalleMaintenance,
        lieu, modele, fournisseur, fabricant, statut
      };
    },


    others_documents() {
      const documents_failure = (this.equipement.liste_documents_defaillance || []).map(doc => ({
        type: 'Demande de BT',
        nomDocument: doc.nomDocumentDefaillance,
        lienDocument: doc.lienDocumentDefaillance
      }));
      const documents_intervention = (this.equipement.liste_documents_intervention || []).map(doc => ({
        type: 'Intervention',
        nomDocument: doc.nomDocumentIntervention,
        lienDocument: doc.lienDocumentIntervention
      }));
      return [...documents_failure, ...documents_intervention];
    }
  },

  methods: {
    get_status_color: getStatusColor,


    format_date(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }).replace(',', '');
    },
    
    format_label(key) {
      const labels = {
        reference: 'Référence',
        designation: 'Désignation',
        dateMiseEnService: 'Date de mise en service',
        prixAchat: 'Prix d\'achat',
        preventifGlissant: 'Préventif glissant',
        joursIntervalleMaintenance: 'Intervalle de maintenance (jours)',
        lieu: 'Lieu',
        modele: 'Modèle',
        fournisseur: 'Fournisseur',
        fabricant: 'Fabricant',
        statut: 'Statut'
      };
      return labels[key] || key;
    },

    format_value(value) {
      if (typeof value === 'boolean') {
        return value ? 'Oui' : 'Non';
      }
      if (typeof value === 'number') {
        return value.toLocaleString();
      }
      return value;
    },

    view_intervention(intervention) {
      this.router.push({
        name: 'InterventionDetail',
        params: { id: intervention.id }
      });
    },

    // edit_equipment() {
    //   this.router.push({
    //     name: 'EditEquipment',
    //     params: { equipementReference: this.equipement.reference }
    //   });
  
    // },

    signal_failure() {
      this.router.push({
        name: 'CreateFailure',
        params: { equipementReference: this.equipement.reference }
      });
    },

    download_document(lien, nomFichier) {
        const cleaned_link = lien.startsWith('/media/') ? lien : `/media/${lien.split('/media/').pop()}`;
        const full_url = `${BASE_URL}${cleaned_link}`;

        fetch(full_url)
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.blob();
          })
          .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = nomFichier;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
          })
          .catch(error => {
            alert('Erreur lors du téléchargement du fichier. Veuillez réessayer.');
          });
      },
    
  },

  created() {
    this.fetch_equipment_data();
  }
};



</script>

<style scoped>
.text-primary {
  color: #05004E;
}

.text-dark {
  color: #3C3C3C;
}

.v-card {
  background-color: #FFFFFF;
}

.v-btn {
  background-color: #F1F5FF;
}

.eye-icon {
  width: 24px;
  height: 24px;
}

h1 {
  color: #05004E;
}
</style>
