<template>
  <v-app>
    <v-main>
      <v-container>
        <h1 class="mb-4">Creer un Equipement</h1>
        <v-form @submit.prevent="submit_form">
          <v-text-field
            v-model="form_data.reference"
            label="Référence"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="form_data.designation"
            label="Désignation"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <v-menu
            ref="menu"
            v-model="date_service_start_menu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="form_data.dateMiseEnService"
                label="Date de mise en service"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                outlined
                dense
                class="mb-4"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="form_data.dateMiseEnService"
              @input="date_service_start_menu = false"
              no-title
              scrollable
            >
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="date_service_start_menu = false">
                Cancel
              </v-btn>
              <v-btn text color="primary" @click="$refs.menu.save(form_data.dateMiseEnService)">
                OK
              </v-btn>
            </v-date-picker>
          </v-menu>

          <v-text-field
            v-model="form_data.prixAchat"
            label="Prix Achat"
            type="number"
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <v-file-input
            label="Image de l'Equipement"
            outlined
            dense
            class="mb-4"
            @change="handle_file_upload"
          ></v-file-input>

          <v-text-field
            v-model="form_data.joursIntervalleMaintenance"
            label="Intervalle de la maintenance (jours)"
            type="number"
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <v-switch
            v-model="form_data.preventifGlissant"
            label="Intervention Préventive Glissante"
            class="mb-4"
          ></v-switch>

          <v-select
            v-model="form_data.modeleEquipement"
            :items="equipment_models"
            item-text="nomModeleEquipement"
            item-title="nomModeleEquipement"
            item-value="id"
            label="Modele de l'Equipement"
            outlined
            dense
            class="mb-4"
          ></v-select>

          <v-select
            v-model="form_data.fournisseur"
            :items="suppliers"
            item-text="nomFournisseur"
            item-title="nomFournisseur"
            item-value="id"
            label="Fournisseur"
            outlined
            dense
            class="mb-4"
          ></v-select>

          <div>
            <h3 class="mb-2">Selectionner un lieu</h3>
            <p v-if="!locations_with_all || locations_with_all.length === 0">Pas de données disponibles.</p>
            <v-treeview
              v-else
              :items="locations_with_all"
              item-key="id"
              :open-on-click="false"
              item-text="nomLieu"
              rounded
              hoverable
              activatable
              dense
            >
              <template v-slot:prepend="{ item, open }">
                <v-icon
                  v-if="item.children && item.children.length > 0 && item.nomLieu !== 'Tous'"
                  @click.stop="toggle_node(item)"
                  :class="{ 'rotate-icon': open }"
                >
                  {{ open ? 'mdi-triangle-down' : 'mdi-triangle-right' }}
                </v-icon>
                <span v-else class="tree-icon-placeholder"></span>
                <span @click="on_click_equipment(item)">{{ item.nomLieu }}</span>
              </template>
              <template v-slot:label="{ item }">
                <span class="text-caption ml-2">{{ item.typeLieu }}</span>
              </template>
            </v-treeview>
          </div>

          <div class="mt-4">
            <h3 class="mb-2">Consommables Associés</h3>
            <v-select
              v-model="selected_consumables"
              :items="consumables"
              item-text="designation"
              item-title="designation"
              item-value="id"
              label="Selectionner le consommable"
              multiple
              chips
              outlined
              dense
            ></v-select>
          </div>

          <v-row justify="end">
            <v-btn color="secondary" class="mt-4 rounded" @click="go_back" style="border-radius: 0; margin-right: 35px;" large>
              Annuler
            </v-btn>
            <v-btn type="submit" color="primary" class="mt-4 rounded" style="border-radius: 0; margin-right: 35px;" large>
              Creer un Equipement
            </v-btn>
          </v-row>
        </v-form>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref, computed, reactive, onMounted, toRefs } from 'vue';
import { useRouter } from 'vue-router';
import { VTreeView } from 'vuetify/labs/components';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  name: 'CreateEquipment',
  components: {
    VTreeView,
  },
  setup() {
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    const state = reactive({
      form_data: {
        reference: "",
        designation: "",
        dateCreation: new Date().toISOString(),
        dateMiseEnService: new Date().toISOString().substr(0, 10),
        prixAchat: null,
        lienImageEquipement: null,
        preventifGlissant: false,
        joursIntervalleMaintenance: null,
        createurEquipement: 1, 
        lieu: null,
        modeleEquipement: null,
        fournisseur: null,
      },
      locations: [],
      equipment_models: [],
      suppliers: [],
      consumables: [],
      selected_consumables: [],
      open_nodes: new Set(),
      date_service_start_menu: false,
    });

    const locations_with_all = computed(() => {
      return [...state.locations];
    });

    const on_click_equipment = (item) => {
      if (state.form_data.lieu && state.form_data.lieu.id === item.id) {
        state.form_data.lieu = null;
      } else {
        state.form_data.lieu = item;
      }
    };

    const toggle_node = (item) => {
      if (state.open_nodes.has(item.id)) {
        state.open_nodes.delete(item.id);
      } else {
        state.open_nodes.add(item.id);
      }
    };

    const submit_form = async () => {
      try {

        state.form_data.dateCreation = new Date().toISOString();

        if (!state.form_data.reference || !state.form_data.designation) {
          return;
        }

        // Création de form_data
        const form_data = new FormData();
        for (const key in state.form_data) {
          if (state.form_data[key] !== null && key !== "lienImageEquipement") {
            if (key == "lieu" ) {
              form_data.append(key, state.form_data.lieu.id.toString());
            }
            else {
              form_data.append(key, state.form_data[key]);
            }
          }
        }

        // Vérification et ajout de l'image
        if (state.form_data.lienImageEquipement instanceof File) {
          form_data.append("lienImageEquipement", state.form_data.lienImageEquipement);
        } else {
          console.warn("Aucun fichier valide détecté.");
        }

       
        for (let pair of form_data.entries()) {
          console.log(pair[0], pair[1]);
        }

        // Envoi avec multipart/form-data
        const response = await api.post('equipements/', form_data, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        if (response) {

          const equipement_id = response.reference; // Récupération de l'ID de l'équipement créé

          // Création de l'objet InformationStatut
          const information_statut_data = {
            statutEquipement: "En fonctionnement",
            dateChangement: new Date().toISOString(),
            equipement: equipement_id,
            informationStatutParent: null, // Ou une valeur par défaut si nécessaire
            ModificateurStatut: 1, // ID fixe du modificateur
          };

          // Envoi de l'information de statut
          const statut_response = await api.post('information-statuts/', information_statut_data, {
            headers: { "Content-Type": "application/json" },
          });

          if (statut_response) {
            for (const consumable_id of state.selected_consumables) {
              await api.post('constituer/', {
                equipement: equipement_id,
                consommable: consumable_id
              });
            }
          }

          go_back();
        } else {
          console.log("Erreur lors de l'ajout de l'équipement.");
        }
      } catch (error) {
        console.error("Erreur lors de la soumission du formulaire:", error);
      }
    };

    const fetchData = async () => {
      try {
        const locationsApi = useApi(API_BASE_URL);
        const modelsApi = useApi(API_BASE_URL);
        const suppliersApi = useApi(API_BASE_URL);
        const consumablesApi = useApi(API_BASE_URL);
        
        await Promise.all([
          locationsApi.get('lieux-hierarchy/'),
          modelsApi.get('modele-equipements/'),
          suppliersApi.get('fournisseurs/'),
          consumablesApi.get('consommables/')
        ]);
        state.locations = locationsApi.data.value;
        state.equipment_models = modelsApi.data.value;
        state.suppliers = suppliersApi.data.value;
        state.consumables = consumablesApi.data.value;
      } catch (error) {
        console.error('Error loading data:', error);
      }
    };

    const handle_file_upload = (event) => {
      const file = event.target.files ? event.target.files[0] : event;
      if (file) {
        state.form_data.lienImageEquipement = file;
      } else {
        console.error("Aucun fichier sélectionné !");
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      fetchData();
    });

    return {
      ...toRefs(state),
      submit_form,
      locations_with_all,
      on_click_equipment,
      toggle_node,
      go_back,
      handle_file_upload
    };
  },
};
</script>