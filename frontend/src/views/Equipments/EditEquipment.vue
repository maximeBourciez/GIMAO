<template>
  <v-app>
    <v-main>
      <v-container v-if="!is_loading">
        <v-row>
          <!-- Left Section: Equipment Details -->
          <v-col cols="6">
            <v-card elevation="1" class="rounded-lg pa-2">
              <v-card-title class="font-weight-bold text-uppercase text-primary">Equipment Description</v-card-title>

              <v-row class="pa-2">
                <v-col cols="12" v-for="(value, key) in equipment_details" :key="key">
                  <p><strong>{{ format_label(key) }} :</strong> {{ format_value(value) }}</p>
                </v-col>
              </v-row>

              <!-- Documentation Section -->
              <v-card elevation="1" class="rounded-lg pa-2 mt-4">
                <v-card-title class="font-weight-bold text-uppercase text-primary">Documentation</v-card-title>

                <!-- Technical Documents -->
                <v-card-subtitle class="pt-4">Technical Documents</v-card-subtitle>
                <v-data-table
                  :headers="technical_documents_headers"
                  :items="equipment.list_documents_techniques"
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
                          <v-icon>mdi-download</v-icon>
                        </v-btn>
                      </td>
                    </tr>
                  </template>
                </v-data-table>

                <!-- Other Documents -->
                <v-card-subtitle class="pt-4">Other Documents</v-card-subtitle>
                <v-data-table
                  :headers="other_documents_headers"
                  :items="other_documents"
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
                          <v-icon>mdi-download</v-icon>
                        </v-btn>
                      </td>
                    </tr>
                  </template>
                </v-data-table>
              </v-card>
            </v-card>
          </v-col>

          <!-- Right Section: Image, Consumables, Maintenance, and Actions -->
          <v-col cols="6">
            <!-- Image Section -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-img
                :src="equipment.lienImageEquipement"
                aspect-ratio="4/3"
                class="rounded-lg"
                style="max-height: 30vh;"
                alt="Equipment Image"
              ></v-img>
            </v-card>
            
            <!-- Consumables Section -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">
                Consumables
              </v-card-title>
              <v-data-table
                :items="equipment.liste_consommables"
                :headers="consumables_headers"
                class="elevation-1 rounded-lg"
                hide-default-footer
              ></v-data-table>
            </v-card>

            <!-- Maintenance History -->
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">
                Interventions
              </v-card-title>
              <v-data-table
                :items="equipment.liste_interventions"
                :headers="interventions_headers"
                class="elevation-1 rounded-lg"
                hide-default-footer
              >
                <template v-slot:item.dateAssignation="{ item }">
                  {{ format_date(item.dateAssignation) }}
                </template>
                <template v-slot:item.action="{ item }">
                  <v-btn icon @click="view_intervention(item)">
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card>

            <!-- Action Button -->
            <v-row justify="end">
              <v-btn color="primary" class="mt-4" large @click="edit_equipment">
                Edit
              </v-btn>
            </v-row>
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
import api, { BASE_URL } from '@/services/api';
import { useRouter } from 'vue-router';

export default {
  name: 'EditEquipment',
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      is_loading: true,
      equipment: {},
      technical_documents_headers: [
        { title: "Technical Document", value: "nomDocumentTechnique", align: "start" },
        { title: "Download", value: "action", align: "center", sortable: false }
      ],
      other_documents_headers: [
        { title: "Type", value: "type", align: "start" },
        { title: "Document", value: "nomDocument", align: "start" },
        { title: "Download", value: "action", align: "center", sortable: false }
      ],
      consumables_headers: [
        { title: "Designation", value: "designation" },
        { title: "Manufacturer", value: "fabricant.nomFabricant" }
      ],
      interventions_headers: [
        { title: "Name", value: "nomIntervention" },
        { title: "Assignment Date", value: "dateAssignation" },
        { title: "View", value: "action" }
      ]
    };
  },
  
  computed: {
    equipment_details() {
      if (!this.equipment) return {};
      const { 
        reference, designation, dateMiseEnService, prixAchat, 
        preventifGlissant, joursIntervalleMaintenance
      } = this.equipment;
      const location = this.equipment.lieu ? this.equipment.lieu.nomLieu : '';
      const model = this.equipment.modeleEquipement ? this.equipment.modeleEquipement.nomModeleEquipement : '';
      const supplier = this.equipment.fournisseur ? this.equipment.fournisseur.nomFournisseur : '';
      const manufacturer = this.equipment.fabricant ? this.equipment.fabricant.nomFabricant : '';
      const status = this.equipment.dernier_statut ? this.equipment.dernier_statut.statutEquipement : '';
      
      return { 
        reference, designation, dateMiseEnService, prixAchat, 
        preventifGlissant, joursIntervalleMaintenance,
        location, model, supplier, manufacturer, status
      };
    },
    other_documents() {
      const failure_documents = (this.equipment.liste_documents_defaillance || []).map(doc => ({
        type: 'Failure',
        nomDocument: doc.nomDocumentDefaillance,
        lienDocument: doc.lienDocumentDefaillance
      }));
      const intervention_documents = (this.equipment.liste_documents_intervention || []).map(doc => ({
        type: 'Intervention',
        nomDocument: doc.nomDocumentIntervention,
        lienDocument: doc.lienDocumentIntervention
      }));
      return [...failure_documents, ...intervention_documents];
    }
  },

  methods: {
    async fetch_equipment_data() {
      try {
        const response = await api.getEquipementAffichage(this.$route.params.reference);
        this.equipment = response.data;
        this.is_loading = false;
      } catch (error) {
        console.error("Error fetching equipment data:", error);
        this.is_loading = false;
      }
    },
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
        reference: 'Reference',
        designation: 'Designation',
        dateMiseEnService: 'Service Start Date',
        prixAchat: 'Purchase Price',
        preventifGlissant: 'Sliding Preventive',
        joursIntervalleMaintenance: 'Maintenance Interval (days)',
        lieu: 'Location',
        modele: 'Model',
        fournisseur: 'Supplier',
        fabricant: 'Manufacturer',
        statut: 'Status'
      };
      return labels[key] || key;
    },

    format_value(value) {
      if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
      }
      if (typeof value === 'number') {
        return value.toLocaleString();
      }
      return value;
    },

    download_document(lien, nom_fichier) {
      const cleanedLink = lien.startsWith('/media/') ? lien : `/media/${lien.split('/media/').pop()}`;
      const fullUrl = `${BASE_URL}${cleanedLink}`;

      fetch(fullUrl)
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
          a.download = nom_fichier;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
        })
        .catch(error => {
          alert('Error downloading the file. Please try again.');
        });
    },

    view_intervention(intervention) {
      this.router.push({
        name: 'InterventionDetail',
        params: { id: intervention.id }
      });
    },

    edit_equipment() {
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
  border-radius: 50%;
}

.eye-icon {
  width: 24px;
  height: 24px;
}

h1 {
  color: #05004E;
}
</style>