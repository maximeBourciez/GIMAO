<template>
  <v-app>
    <v-main>
      <v-container>
        <v-form @submit.prevent="submit_form">

          <!-- Error Message with v-alert at the top -->
          <v-alert v-if="error_message" type="error" class="mt-4">
            {{ error_message }}
          </v-alert>

          <v-text-field
            v-model="form_data.location_name"
            label="Nom du Lieu"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="form_data.location_type"
            label="Type du lieu"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <div>
            <p v-if="!places_with_all || places_with_all.length === 0">Pas de données disponibles.</p>
            <v-treeview
              v-else
              :items="places_with_all"
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
                <span @click="on_click_location(item)">{{ item.nomLieu }}</span>
              </template>
              <template v-slot:label="{ item }">
                <span class="text-caption ml-2">{{ item.typeLieu }}</span>
              </template>
            </v-treeview>
          </div>

          <v-row justify="end">
            <v-btn color="secondary" class="mt-4 rounded" @click="go_back" style="border-radius: 0; margin-right: 35px;" large>
              Annuler
            </v-btn>
            <v-btn type="submit" color="primary" class="mt-4 rounded" :disabled="!is_form_valid" style="border-radius: 0 ;margin-right: 35px;" large>
              Ajouter Lieu
            </v-btn>
          </v-row>

        </v-form>
      </v-container>
    </v-main>
  </v-app>
</template>


<script>
import api from '@/services/api';
import { ref, computed, reactive, onMounted, toRefs } from 'vue';
import { useRouter } from 'vue-router';
import { VTreeView } from 'vuetify/labs/components';

export default {
  name: 'CreateLocation',
  components: {
    VTreeView,
  },
  setup() {
    const router = useRouter();
    const state = reactive({
      form_data: {
        location_name: "",
        location_type: "",
        location: null,
        header: [
          { title: 'Location', value: 'location.nomLieu', sortable: true, align: 'center' },
        ],
        open_nodes: new Set(),
      },
      locations: [],
      error_message: "" // Add error message state
    });

    const places_with_all = computed(() => {
      return [...state.locations];
    });

    const on_click_location = (item) => {
      if (state.form_data.location && state.form_data.location.id === item.id) {
        state.form_data.location = null;
      } else {
        state.form_data.location = item;
      }
    };

    const toggle_node = (item) => {
      if (state.open_nodes.has(item.id)) {
        state.open_nodes.delete(item.id);
      } else {
        state.open_nodes.add(item.id);
      }
    };

    const is_form_valid = computed(() => {
      return state.form_data.location_name &&
             state.form_data.location_type;
    });

    const submit_form = async () => {
      if (!is_form_valid.value) {
        state.error_message = 'Veuillez remplir tous les champs requis.';
        return;
      }

      state.error_message = ""; // Clear error message if form is valid

      const form_data = new FormData();
      form_data.append('nomLieu', state.form_data.location_name);
      form_data.append('typeLieu', state.form_data.location_type);

      if (state.form_data.location) {
        form_data.append('lieuParent', state.form_data.location.id);
      }

      try {
        const responseLieu = await api.postLieu(form_data);
        if (responseLieu.status === 201) {
          go_back();
        } else {
          state.error_message = 'Une erreur est survenue lors de la création du lieu.';
        }
      } catch (error) {
        console.error('Error creating lieu:', error);
        state.error_message = 'Une erreur est survenue lors de la création du lieu.';
      }
    };

    const fetch_data = async () => {
      try {
        const [locationRES] = await Promise.all([api.getLieuxHierarchy()]);
        state.locations = locationRES.data;
      } catch (error) {
        console.error('Error loading data:', error);
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      fetch_data();
    });

    return {
      ...toRefs(state),
      submit_form,
      places_with_all,
      on_click_location,
      toggle_node,
      go_back,
      is_form_valid
    };
  },
};
</script>
