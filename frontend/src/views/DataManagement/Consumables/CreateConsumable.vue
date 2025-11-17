<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Ajouter un nouveau consommable</v-card-title>
          <v-card-text>
            <!-- Error Alert -->
            <v-alert v-if="error_message" type="error" class="mb-4">
              {{ error_message }}
            </v-alert>

            <!-- Loading Alert -->
            <v-alert v-if="is_loading" type="info" class="mb-4">
              Chargement des fabricants...
            </v-alert>

            <v-form @submit.prevent="submit_form">
              <v-text-field
                v-model="consumable.designation"
                label="Désignation"
                required
              ></v-text-field>

              <v-file-input
                v-model="consumable.lienImageConsommable"
                label="Image du consommable"
                accept="image/jpeg, image/png"
                prepend-icon="mdi-camera"
              ></v-file-input>

              <v-select
                v-if="!is_loading && fabricants.length > 0"
                v-model="consumable.fabricant"
                :items="fabricants"
                item-title="nomFabricant"
                item-value="id"
                label="Fabricant"
                required
                return-object
              ></v-select>

              <v-btn color="secondary" class="mt-4 mr-2" @click="go_back">
                Retour
              </v-btn>
              <v-btn type="submit" color="primary" class="mt-4" :disabled="!is_form_valid">
                Ajouter le consommable
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  setup() {
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    const fabricantsApi = useApi(API_BASE_URL);
    const consumable = ref({
      designation: '',
      lienImageConsommable: null,
      fabricant: null
    });
    const fabricants = ref([]);
    const error_message = ref('');
    const is_loading = ref(false);

    const is_loading = computed(() => fabricantsApi.loading.value);

    const is_form_valid = computed(() => {
      return consumable.value.designation &&
             consumable.value.fabricant &&
             consumable.value.lienImageConsommable;
    });

    const get_manufacturers = async () => {
      error_message.value = '';
      try {
        const response = await fabricantsApi.get('fabricants/');
        fabricants.value = response;
      } catch (error) {
        console.error('Error fetching fabricants:', error);
        error_message.value = 'Erreur lors de la récupération des fabricants.';
      }
    };

    const submit_form = async () => {
      if (!is_form_valid.value) {
        error_message.value = 'Veuillez remplir tous les champs requis.';
        return;
      }

      try {
        const formData = new FormData();
        formData.append('designation', consumable.value.designation);
        formData.append('fabricant', consumable.value.fabricant.id);
        if (consumable.value.lienImageConsommable) {
          formData.append('lienImageConsommable', consumable.value.lienImageConsommable);
        }

        await api.post('consommables/', formData);

        go_back();
      } catch (error) {
        console.error('Error creating consommable:', error);
        error_message.value = "Une erreur est survenue lors de l'ajout du consommable.";
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    const handle_file_change = (file) => {
      consumable.value.lienImageConsommable = file;
    };

    onMounted(() => {
      get_manufacturers();
    });

    return {
      consumable,
      fabricants,
      error_message,
      is_loading,
      is_form_valid,
      submit_form,
      go_back,
      handle_file_change
    };
  }
};
</script>
