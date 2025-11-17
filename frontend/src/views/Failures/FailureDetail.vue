<template>
  <v-app>
    <v-main>
      <v-container class="py-5">
        <v-card class="pa-4">
          <v-row v-if="defaillance">
            <!-- Colonne de gauche avec les informations -->
            <v-col cols="6" class="column-offset">
              <v-row>
                <v-col cols="12" v-for="(value, key) in formatted_failure_label" :key="key">
                  <p>
                    <strong>{{ key }} : </strong>
                    <v-chip v-if="key === 'Niveau'" :color="get_niveau_color(value)" small>
                      {{ value }}
                    </v-chip>
                    <v-chip v-else-if="key === 'Traitée'" :color="get_type_color(value)" small>
                      {{ value }}
                    </v-chip>
                    <span v-else>{{ value }}</span>
                  </p>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-select
                    v-model="selected_status"
                    :items="status_options"
                    label="Changer le statut de l'équipement"
                  ></v-select>
                </v-col>
              </v-row>
                
              
            </v-col>

            <!-- Colonne de droite avec les informations supplémentaires -->
            <v-col cols="6">
              <v-row>
                <!-- Section pour l'équipement associé -->
                <v-col cols="12">
                  <v-card
                    class="mt-4 pa-4"
                    elevation="2"
                    @click="toggle_equipment_details"
                    :class="{ 'expanded': show_equipment_details }"
                  >
                    <v-card-title class="text-h6 d-flex align-center">
                      Équipement
                      <v-spacer></v-spacer>
                      <v-btn
                        color="primary"
                        class="ml-2"
                        @click.stop="open_equipment"
                        :disabled="!defaillance.equipement"
                      >
                        Détails
                      </v-btn>
                      <v-icon class="ml-2">
                        {{ show_equipment_details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                      </v-icon>
                    </v-card-title>
                    <v-expand-transition>
                      <div v-show="show_equipment_details">
                        <v-divider class="my-2"></v-divider>
                        <v-card-text>
                          <v-row>
                            <v-col cols="12" v-for="(value, key) in formatted_equipment_label" :key="key">
                              <p><strong>{{ key }} :</strong> {{ value }}</p>
                            </v-col>
                          </v-row>
                        </v-card-text>
                      </div>
                    </v-expand-transition>
                  </v-card>
                </v-col>

                <!-- Section pour les Documents de défaillance -->
                <v-col cols="12">
                  <v-card
                    class="mt-4 pa-4"
                    elevation="2"
                  >
                    <v-card-title class="text-h6 d-flex align-center">
                      Documents de la défaillance
                      <v-spacer></v-spacer>
                      <v-btn
                        color="primary"
                        small
                        class="mr-2"
                        @click.stop="add_document"
                      >
                        Ajouter
                      </v-btn>
                      <v-btn
                        @click.stop="toggle_documents_details"
                      >
                        <v-icon class="ml-2">
                          {{ show_documents_details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                        </v-icon>
                      </v-btn>
                    </v-card-title>
                    <v-expand-transition>
                      <div v-show="show_documents_details">
                        <v-divider class="my-2"></v-divider>
                        <v-card-text>
                          <v-data-table
                            :headers="headers"
                            :items="defaillance.liste_documents_defaillance || []"
                            class="elevation-1"
                            hide-default-footer
                            :items-per-page="-1"
                          >
                            <template v-slot:top>
                              <v-toolbar flat>
                                <v-spacer></v-spacer>
                                <v-btn color="primary" small @click="toggle_action_mode">
                                  {{ action_mode === 'download' ? 'Mode suppression' : 'Mode téléchargement' }}
                                </v-btn>
                              </v-toolbar>
                            </template>

                            <template v-slot:item.actions="{ item }">
                              <v-btn
                                icon
                                small
                                :color="action_mode === 'download' ? 'primary' : 'error'"
                                @click="action_mode === 'download' ? download_document(item) : delete_document(item)"
                              >
                                <v-icon small>
                                  {{ action_mode === 'download' ? 'mdi-download' : 'mdi-delete' }}
                                </v-icon>
                              </v-btn>
                            </template>
                          </v-data-table>
                        </v-card-text>
                      </div>
                    </v-expand-transition>
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
          </v-row>

          <!-- Boutons -->
          <v-row justify="center" class="mt-4">
            <v-btn color="primary" class="text-white mx-2" @click="go_back">
              Retour
            </v-btn>

            <v-btn color="error" class="text-white mx-2" @click="delete_failure" :disabled="!can_delete">
              Supprimer la demande
            </v-btn>

            <v-btn color="success" class="text-white mx-2" @click="treat_failure" :disabled="!can_treat">
              Mettre en attente la demande
            </v-btn>

            <v-btn color="success" class="text-white mx-2" @click="create_intervention" :disabled="can_treat">
              Transformer en bon de travail
              
            </v-btn>
          </v-row>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { getFailureLevelColor } from '@/utils/helpers';
import { API_BASE_URL, BASE_URL } from '@/utils/constants';

export default {
  name: 'FailureDetail',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const failureApi = useApi(API_BASE_URL);
    const equipmentApi = useApi(API_BASE_URL);
    const patchApi = useApi(API_BASE_URL);
    const statutApi = useApi(API_BASE_URL);
    const defaillance = ref(null);
    const show_equipment_details = ref(false);
    const show_documents_details = ref(false);
    const action_mode = ref('download');
    const selected_status = ref("pas de changement");

    const go_back = () => {
      router.go(-1);
    };

    const headers = [
      { title: 'Nom du document', value: 'nomDocumentDefaillance' },
      { title: 'Actions', value: 'actions', sortable: false }
    ];

    const toggle_action_mode = () => {
      action_mode.value = action_mode.value === 'download' ? 'delete' : 'download';
    };

    const delete_document = async (item) => {
    if (confirm(`Êtes-vous sûr de vouloir supprimer le document "${item.nomDocumentDefaillance}" ?`)) {
      try {
  
        // Rafraîchir la liste des documents après la suppression
        await fetch_data();
        
        // Afficher un message de succès
        alert(`Le document "${item.nomDocumentDefaillance}" a été supprimé avec succès.`);
      } catch (error) {
        console.error('Erreur détaillée lors de la suppression du document:', error);
        let errorMessage = 'Une erreur est survenue lors de la suppression du document.';
        
        if (error.response) {
          console.error('Réponse d\'erreur du serveur:', error.response);
          if (error.response.data && error.response.data.message) {
            errorMessage = error.response.data.message;
          } else {
            errorMessage = `Erreur ${error.response.status}: ${error.response.statusText}`;
          }
        } else if (error.request) {
          console.error('Pas de réponse reçue:', error.request);
          errorMessage = "Le serveur ne répond pas. Veuillez réessayer plus tard.";
        } else {
          console.error('Erreur de configuration de la requête:', error.message);
        }
        
        // Afficher l'erreur à l'utilisateur
        alert(errorMessage);
      }
    }
  };

  const fetch_data = async () => {
    try {
      const response = await failureApi.get(`defaillance/${route.params.id}/affichage/`);
      const defaillanceData = response;

      if (defaillanceData.equipement && typeof defaillanceData.equipement === 'object') {
        defaillanceData.equipement.dernier_statut = defaillanceData.equipement.dernier_statut || {};
      } else if (typeof defaillanceData.equipement === 'string') {
        const equipementResponse = await equipmentApi.get(`equipement/${defaillanceData.equipement}/affichage/`);
        defaillanceData.equipement = equipementResponse;
        defaillanceData.equipement.dernier_statut = defaillanceData.equipement.dernier_statut || {};
      } else {
        console.error('Les données de l\'équipement sont manquantes ou invalides');
        defaillanceData.equipement = { dernier_statut: {} };
      }

      // Mettre à jour defaillance.value avec les données complètes
      defaillance.value = defaillanceData;

    } catch (error) {
      console.error('Erreur lors de la récupération des données:', error);
    }
  };

    const get_niveau_color = (level) => {
      switch (level) {
        case 'Critique':
          return 'red';
        case 'Majeur':
          return 'orange';
        default:
          return 'green';
      }
    };

    const get_type_color = (color) => {
      switch (color) {
        case 'Oui':
          return 'green';
        default:
          return 'red';
      }};


    const format_date = (dateString) => {
      if (!dateString) return 'Non spécifié';
      const date = new Date(dateString);
      return date.toLocaleString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const formatted_failure_label = computed(() => {
      if (!defaillance.value) return {};
      const label = {
        'Description': defaillance.value.commentaireDefaillance,
        'Niveau': defaillance.value.niveau,
        'Traitée': defaillance.value.dateTraitementDefaillance ? 'Oui' : 'Non',
        // 'Utilisateur': defaillance.value.utilisateur?.username || 'Non spécifié',
      };
          
      if (defaillance.value.dateTraitementDefaillance) {
        label['Date de traitement'] = format_date(defaillance.value.dateTraitementDefaillance);
      }

      if (defaillance.value.intervention) {
        label['Intervention créée le '] = format_date(defaillance.value.intervention.dateAssignation);
      }

      return label;
    });

    const formatted_equipment_label = computed(() => {
      if (!defaillance.value || !defaillance.value.equipement) return {};
      const equipement = defaillance.value.equipement;
      return {
        'Référence': equipement.reference || 'Non spécifié',
        'Désignation': equipement.designation || 'Non spécifié',
        'Statut': equipement.dernier_statut?.statutEquipement || 'Non spécifié',
        'Date de mise en service': equipement.dateMiseEnService ? format_date(equipement.dateMiseEnService) : 'Non spécifié',
        'Prix d\'achat': equipement.prixAchat ? `${equipement.prixAchat} €` : 'Non spécifié',
        'Préventif glissant': equipement.preventifGlissant !== undefined ? (equipement.preventifGlissant ? 'Oui' : 'Non') : 'Non spécifié',
        'Intervalle de maintenance': equipement.joursIntervalleMaintenance ? `${equipement.joursIntervalleMaintenance} jours` : 'Non spécifié',
      };
    });
    
    const can_delete = computed(() => {
      return defaillance.value && !defaillance.value.intervention;
    });

    const can_treat = computed(() => {
      return defaillance.value && !defaillance.value.dateTraitementDefaillance;
    });


    const delete_failure = async () => {
      if (!can_delete.value) {
        alert("Impossible de supprimer cette défaillance car une intervention est déjà associée.");
        return;
      }

      if (confirm('Êtes-vous sûr de vouloir supprimer cette défaillance et tous ses documents associés ?')) {
        try {
          // Supprimer d'abord tous les documents associés
          if (defaillance.value.documents && defaillance.value.documents.length > 0) {
            for (const document of defaillance.value.documents) {
              // await api.deleteDefaillanceDocument(document.id);
            }
          }

          // Ensuite, supprimer la défaillance
          // await api.deleteDefaillance(defaillance.value.id);
          
          // Redirection vers la page des signalements
          router.push({ 
            name: 'openEquipmentDetail', 
            params: { reference: defaillance.value.equipement.reference }
          });
        } catch (error) {
          console.error('Erreur lors de la suppression de la défaillance ou de ses documents:', error);
        }
      }
    };

    const treat_failure = async () => {
      if (confirm('Êtes-vous sûr de vouloir traiter cette défaillance ?')) {
        try {
          const dateTraitementDefaillance = new Date().toISOString();
          const response = await patchApi.patch(`defaillances/${defaillance.value.id}/`, {
            dateTraitementDefaillance: dateTraitementDefaillance
          });
          
          defaillance.value = { 
            ...defaillance.value, 
            ...response,
            equipement: defaillance.value.equipement 
          };

          if (selected_status.value !== "pas de changement" || selected_status.value == defaillance.value.equipement?.dernier_statut.statutEquipement ) {
            const statutData = {
              statutEquipement: selected_status.value,
              dateChangement: new Date().toISOString(),
              equipement: defaillance.value.equipement?.reference,
              informationStatutParent: defaillance.value.equipement.dernier_statut.id,
              ModificateurStatut: 1
            };

            await statutApi.post('information-statuts/', statutData);
          }

          await fetch_data();
          
        } catch (error) {
          console.error('Erreur lors du traitement de la défaillance:', error);
        }
      }
    };

    const create_intervention = () => {
      if (defaillance.value && defaillance.value.id) {
        router.push({ 
          name: 'CreateIntervention', 
          params: { id: defaillance.value.id }
        });
      } else {
        console.error("ID de défaillance manquant");
        alert("Impossible de créer une intervention. Données de défaillance manquantes.");
      }
    };

    const toggle_equipment_details = () => {
      show_equipment_details.value = !show_equipment_details.value;
    };

    const toggle_documents_details = () => {
      show_documents_details.value = !show_documents_details.value;
    };

    const add_document = () => {
      router.push({ 
        name: 'AddDocumentFailure', 
        params: { id: defaillance.value.id }
      });
    };

    const open_equipment = () => {
      if (defaillance.value && defaillance.value.equipement) {
        router.push({ 
          name: 'EquipmentDetail', 
          params: { reference: defaillance.value.equipement.reference }
        });
      }
    };

    const download_document = (item) => {
      const cleanedLink = item.lienDocumentDefaillance.startsWith('/media/') 
        ? item.lienDocumentDefaillance 
        : `/media/${item.lienDocumentDefaillance.split('/media/').pop()}`;
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
          a.download = item.nomDocumentDefaillance;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
        })
        .catch(error => {
          console.error('Erreur lors du téléchargement:', error);
          alert('Erreur lors du téléchargement du fichier. Veuillez réessayer.');
        });
    };

  
  
  const status_options = [
    "pas de changement",
    "En fonctionnement",
    "Dégradé",
    "À l'arrêt"
  ];

    onMounted(fetch_data);

    return {
      defaillance,
      formatted_failure_label,
      formatted_equipment_label,
      can_delete,
      can_treat,
      delete_failure,
      treat_failure,
      create_intervention,
      show_equipment_details,
      show_documents_details,
      toggle_equipment_details,
      toggle_documents_details,
      open_equipment,
      headers,
      download_document,
      add_document,
      action_mode,
      toggle_action_mode,
      delete_document,
      get_niveau_color,
      get_type_color,
      go_back,
      selected_status,
      status_options,
    };
  }
};
</script>

<style scoped>
.expanded {
  background-color: #f5f5f5;
}

.column-offset {
  margin-top: 20px; 
}
</style>