<template>
  <v-app>
    <v-main>
      <v-container>
        <v-form @submit.prevent="submit_form">

          <!-- Error Alert -->
          <v-alert v-if="error_message" type="error" class="mb-4">
            {{ error_message }}
          </v-alert>

          <v-text-field
            v-model="form_data.nomModeleEquipement"
            label="Nom du modéle d'équipement"
            required
            outlined
            dense
            class="mb-4"
          ></v-text-field>

          <v-select
            v-model="form_data.fabricant"
            :items="manufacturers"
            item-text="nomFabricant"
            item-title="nomFabricant"
            item-value="id"
            label="Fabricant"
            outlined
            dense
            class="mb-4"
          ></v-select>

          <v-row justify="end">
            <v-btn color="secondary" class="mt-4 rounded" @click="go_back" style="border-radius: 0; margin-right: 35px;" large>
              Annuler
            </v-btn>
            <v-btn type="submit" color="primary" class="mt-4 rounded" style="border-radius: 0 ;margin-right: 35px;" large>
              Ajouter un modéle d'équipement
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

export default {
  name: 'CreateModelEquipment',
  setup() {
    const router = useRouter();
    const state = reactive({
      form_data: {
        nomModeleEquipement: "",
        fabricant: null,
      },
      manufacturers: [],
      error_message: "" // Add error message state
    });

    const submit_form = async () => {
      const form_data = new FormData();
      form_data.append('nomModeleEquipement', state.form_data.nomModeleEquipement);
      form_data.append('fabricant', state.form_data.fabricant);

      try {
        const response = await api.postModeleEquipement(form_data);
        if (response.status === 201) {
          go_back();
        } else {
          state.error_message = 'Erreur lors de la création du modèle d\'équipement.';
        }
      } catch (error) {
        console.error('Error submitting the form:', error);
        state.error_message = 'Une erreur est survenue lors de la soumission du formulaire.';
      }
    };

    const fetch_data = async () => {
      try {
        const [manufacturers_res] = await Promise.all([api.getFabricants()]);
        state.manufacturers = manufacturers_res.data;
      } catch (error) {
        console.error('Error loading data:', error);
        state.error_message = 'Erreur lors du chargement des fabricants.';
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
      go_back,
    };
  },
};
</script>
