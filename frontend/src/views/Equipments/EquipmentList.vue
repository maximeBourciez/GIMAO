<template>
  <v-container>
    <v-row>
      <!-- Left Column -->
      <v-col cols="4">
        <!-- Card: Structure of Locations -->
        <v-card elevation="1" class="rounded-lg pa-2 mb-4">
          <v-card-title class="font-weight-bold text-uppercase text-primary">
            Structure des Lieux
          </v-card-title>
          <v-divider></v-divider>
          <div>
            <!-- Message if no data is available -->
            <p v-if="!locations_with_all || locations_with_all.length === 0">Pas de données disponibles.</p>
            <!-- Treeview of locations -->
            <v-treeview
              v-else
              v-model:selected="selected_tree_nodes"
              :items="locations"
              item-title="nomLieu"
              item-value="id"
              select-strategy="selectionType"
              selectable
              dense
              @update:selected="on_select_location"
            >
              <!-- Slot for the prefix icon (arrow to open/close nodes) -->
              <template v-slot:prepend="{ item, open }">
                <v-icon
                  v-if="item.children && item.children.length > 0 && item.nomLieu !== 'Tous'"
                  @click.stop="toggle_node(item)"
                  :class="{ 'rotate-icon': open }"
                >
                  {{ open ? 'mdi-triangle-down' : 'mdi-triangle-right' }}
                </v-icon>
                <!-- Placeholder for items without children -->
                <span v-else class="tree-icon-placeholder"></span>
              </template>
              <!-- Slot for custom label (display of location type) -->
              <template v-slot:label="{ item }">
                <span class="text-caption ml-2">{{ item.typeLieu }}</span>
              </template>
            </v-treeview>
          </div>
        </v-card>
        
        <!-- Card: Types of Equipment -->
        <v-card elevation="1" class="rounded-lg pa-2">
          <v-card-title class="font-weight-bold text-uppercase text-primary">
            Types des équipements
          </v-card-title>
          <v-divider></v-divider>
          <!-- List of equipment types -->
          <v-list dense>
            <!-- "All" option to select all types of equipment -->
            <v-list-item
              link
              @click="handle_equipment_type_selected(null)"
              :class="{ 'selected-item': selected_type_equipments.length === 0 }"
            >
              <v-list-item-title>Tous</v-list-item-title>
            </v-list-item>
            <!-- Loop to display each type of equipment -->
            <v-list-item
              v-for="(model, index) in equipment_models"
              :key="index"
              link
              @click="handle_equipment_type_selected(model)"
              :class="{ 'selected-item': is_equipment_type_selected(model) }"
            >
              <v-list-item-title>{{ model.nomModeleEquipement }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      
      <!-- Right Column -->
      <v-col cols="8">
        <!-- Button to redirect to the equipment addition page -->
        <v-btn color="primary" @click="open_add_equipment_page" class="mb-4">
          Ajouter un équipement
        </v-btn>

        <!-- Equipment Table -->
        <v-data-table
          :headers="header"
          :items="filtered_equipments"
          :items-per-page="items_per_page"
          :page.sync="page"
          class="elevation-1 rounded-lg"
          @page-count="pageCount = $event"
          :sort-by="['designation']"
          :sort-desc="[false]"
        >
          <!-- Custom template for each row in the table -->
          <template v-slot:item="{ item }">
            <!-- Clickable row to show equipment details -->
            <tr @click="open_view_equipment(item.reference)" style="cursor: pointer;">
              <td>{{ item.designation }}</td>
              <td>{{ item.lieu.nomLieu }}</td>
              <td>
                <v-chip
                  :color="get_status_color(item.statut.statutEquipement)"
                  text-color="white"
                  small
                >
                  {{ item.statut.statutEquipement }}
                </v-chip>
              </td>
            </tr>
          </template>
        </v-data-table>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, onMounted, reactive, toRefs } from 'vue';
import { useRouter } from 'vue-router';
import { VTreeView } from 'vuetify/labs/components';
import api from '@/services/api';

export default {
  name: 'EquipmentList',
  components: {
    VTreeView,
  },
  setup() {
    const router = useRouter();

    // Reactive state to manage data and component state
    const state = reactive({
      equipments: [],
      locations: [],
      equipment_models: [],
      selected_location: [],
      selected_type_equipments: [],
      selected_tree_nodes: [],
      page: 1,
      pageCount: 0,
      items_per_page: 10,
      header: [
        { title: 'Désignation', value: 'modeleEquipement.nomModeleEquipement', sortable: true, align: 'center' },
        { title: 'Lieu', value: 'lieu.nomLieu', sortable: true, align: 'center' },
        { title: 'Statut', value: 'statut.statutEquipement', sortable: true, align: 'center',
          sort: (a, b) => {
            const order = ['Rebuté', 'En fonctionnement', 'Dégradé', 'À l\'arrêt'];
            return order.indexOf(a) - order.indexOf(b);
          }
        },
      ],
      open_nodes: new Set(),
    });

    // Function to fetch data from the API
    const fetchData = async () => {
      try {
        const [equipmentsRes, locationsRes, equipmentModelsRes] = await Promise.all([
          api.getEquipementsVue(),
          api.getLieuxHierarchy(),
          api.getModeleEquipements()
        ]);

        state.equipments = equipmentsRes.data;
        state.locations = locationsRes.data;
        state.equipment_models = equipmentModelsRes.data;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const get_status_color = (status) => {
      switch (status) {
        case 'En fonctionnement':
          return 'green';
        case 'Dégradé':
          return 'orange';
          case 'À l\'arrêt':
          return 'red';
        default:
          return 'black';
      }
    };

    // Compute locations with the "All" option
    const locations_with_all = computed(() => {
      return [{ id: null, nomLieu: 'All' }, ...state.locations];
    });

    // Handle selection of a location in the treeview
    const on_select_location = (items) => {
      if (items.length > 0) {
        state.selected_location = items.map(id => {
          const selectedItem = find_item(locations_with_all.value, id);
          return selectedItem?.nomLieu;
        }).filter(Boolean);
      } else {
        state.selected_location = [];
      }
    };

    // Function to find an item in the treeview
    const find_item = (items, id) => {
      for (const item of items) {
        if (item.id === id) {
          return item;
        }
        if (item.children) {
          const found = find_item(item.children, id);
          if (found) {
            return found;
          }
        }
      }
      return null;
    };

    // Function to toggle the state of a node in the treeview
    const toggle_node = (item) => {
      if (state.open_nodes.has(item.id)) {
        state.open_nodes.delete(item.id);
      } else {
        state.open_nodes.add(item.id);
      }
    };

    // Handle selection of an equipment type
    const handle_equipment_type_selected = (model) => {
      if (model === null) {
        state.selected_type_equipments = [];
      } else {
        const index = state.selected_type_equipments.findIndex(m => m.nomModeleEquipement === model.nomModeleEquipement);
        if (index > -1) {
          state.selected_type_equipments.splice(index, 1);
        } else {
          state.selected_type_equipments.push(model);
        }
      }
    };

    // Check if an equipment type is selected
    const is_equipment_type_selected = (model) => {
      return state.selected_type_equipments.some(m => m.nomModeleEquipement === model.nomModeleEquipement);
    };

    // Filter equipments based on selections
    const filtered_equipments = computed(() => {
      return state.equipments.filter(e => {
        const locationMatch = state.selected_location.length === 0 || 
                           state.selected_location.includes('All') || 
                           state.selected_location.includes(e.lieu.nomLieu);
        const typeMatch = state.selected_type_equipments.length === 0 ||
                         state.selected_type_equipments.some(m => 
                           m.nomModeleEquipement === e.modeleEquipement.nomModeleEquipement
                         );
        return locationMatch && typeMatch;
      });
    });

    // Redirect to the add equipment page
    const open_add_equipment_page = () => {
      router.push('/CreateEquipment');
    };

    // Redirect to the view equipment page
    const open_view_equipment = (reference) => {
      router.push({ name: 'EquipmentDetail', params: { reference: reference } });
    };

    // Load data on component mount
    onMounted(fetchData);

    return {
      ...toRefs(state),
      locations_with_all,
      filtered_equipments,
      on_select_location,
      handle_equipment_type_selected,
      open_add_equipment_page,
      open_view_equipment,
      is_equipment_type_selected,
      toggle_node,
      get_status_color,
    };
  }
};
</script>

<style scoped>
.v-data-table tr:hover {
  background-color: #e6f2ff;
  transition: background-color 0.3s ease;
}

.v-data-table tr:hover td {
  color: #0056b3;
}

.v-data-table th {
  color: black !important;
}

.v-treeview-node--active {
  background-color: #7577e9 !important;
  color: white !important;
}

.v-treeview-node--active:hover {
  background-color: #5658c7 !important;
}

.selected-item {
  background-color: #7577e9 !important;
  color: white !important;
}

.selected-item:hover {
  background-color: #5658c7 !important;
}

.text-caption {
  color: #666;
  font-size: 0.75rem;
}

.tree-icon-placeholder {
  display: inline-block;
  width: 24px;
  height: 24px;
  margin-right: 4px;
}

.rotate-icon {
  transform: rotate(180deg);
}

.v-icon {
  transition: transform 0.3s ease;
}
</style>