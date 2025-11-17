<template>
  <v-app>
    <v-main>
      <v-container class="py-5">
        <v-card class="pa-4">
          <v-form ref="formRef" v-model="form_valid">

            <!-- Error Alert -->
            <v-alert v-if="error_message" type="error" class="mb-4">
              {{ error_message }}
            </v-alert>

            <v-row>
              <v-col cols="6">
                <v-select
                  v-model="form.niveau"
                  label="Niveau"
                  :items="levels"
                  outlined
                  dense
                  :rules="[v => !!v || (validation_triggered && 'Niveau requis')]"
                ></v-select>
              </v-col>
              <v-col cols="6">
                <v-textarea
                  v-model="form.commentaireDefaillance"
                  label="Commentaires"
                  rows="5"
                  outlined
                  counter="300"
                  :rules="[
                    v => !!v.trim() || (validation_triggered && 'Commentaire requis'),
                    v => (v && v.length <= 300) || 'Le commentaire ne doit pas dépasser 300 caractères.',
                    v => (v && v.trim().length > 0) || 'Le commentaire ne doit pas être vide ou contenir uniquement des espaces.'
                  ]"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row justify="center" class="mt-4">
              <v-btn color="primary" class="text-white mx-2" @click="go_back">
                Retour
              </v-btn>
              <v-btn color="primary" class="text-white mx-2" @click="reset_form">
                Effacer
              </v-btn>
              <v-btn color="success" class="text-white mx-2" @click="validate_form">
                Valider
              </v-btn>
            </v-row>
          </v-form>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import '@/assets/css/global.css';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    const api = useApi(API_BASE_URL);
    const equipmentsApi = useApi(API_BASE_URL);
    
    const equipment_list = computed(() => 
      (equipmentsApi.data.value || []).map(eq => ({
        ...eq,
        label: `${eq.reference} - ${eq.designation}`
      }))
    );
    const levels = ['Mineur', 'Majeur', 'Critique'];
    const form = ref({
      equipement: null,
      commentaireDefaillance: "",
      niveau: null,
    });
    const form_valid = ref(false);
    const validation_triggered = ref(false);
    const equipment_reference = ref(null);
    const connected_user = {
      id: 1,
      username: "admin",
      first_name: "admin",
      last_name: "admin",
      email: "admin@a.com",
    };
    const error_message = ref("");
    const formRef = ref(null);

    const fetch_data = async () => {
      try {
        await equipmentsApi.get('equipements/');
      } catch (error) {
        console.error('Erreur lors de la récupération des données:', error);
      }
    };

    const reset_form = () => {
      form.value = {
        equipement: equipment_reference.value || null,
        commentaireDefaillance: "",
        niveau: null,
      };
      validation_triggered.value = false;
      error_message.value = "";
      if (formRef.value) {
        formRef.value.resetValidation();
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    const validate_form = async () => {
      validation_triggered.value = true;
      const formElement = formRef.value;

      if (formElement) {
        formElement.validate();
        if (form_valid.value) {
          try {
            const failure_data = {
              commentaireDefaillance: form.value.commentaireDefaillance,
              niveau: form.value.niveau,
              equipement: form.value.equipement,
              utilisateur: connected_user.id,
              dateTraitementDefaillance: null
            };
            const response = await api.post('defaillances/', failure_data);

            const new_failure_id = response.id;

            router.push({ name: 'FailureDetail', params: { id: new_failure_id } });

          } catch (error) {
            console.error('Erreur lors de la création de la défaillance:', error);
            error_message.value = "Une erreur est survenue lors de la création de la défaillance.";
          }
        } else {
          error_message.value = "Veuillez remplir tous les champs obligatoires.";
        }
      }
    };

    onMounted(async () => {
      await fetch_data();
      equipment_reference.value = route.params.equipementReference;
      if (equipment_reference.value) {
        form.value.equipement = equipment_reference.value;
      }
    });

    return {
      router,
      equipment_list,
      levels,
      form,
      form_valid,
      validation_triggered,
      error_message,
      formRef,
      reset_form,
      go_back,
      validate_form
    };
  },
};
</script>

