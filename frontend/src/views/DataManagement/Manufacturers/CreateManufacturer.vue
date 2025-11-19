<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Ajouter un nouveau fabricant</v-card-title>
          <v-card-text>
            <v-alert v-if="error_message" type="error">
              {{ error_message }}
            </v-alert>
            <v-form @submit.prevent="submit_form">
              <v-text-field
                v-model="manufacturer.nomFabricant"
                label="Nom du fabricant"
                required
              ></v-text-field>

              <v-text-field
                v-model="manufacturer.paysFabricant"
                label="Pays"
                required
              ></v-text-field>

              <v-text-field
                v-model="manufacturer.mailFabricant"
                label="Email"
                type="email"
                required
              ></v-text-field>

              <v-text-field
                v-model="manufacturer.numTelephoneFabricant"
                label="Numéro de téléphone"
                required
              ></v-text-field>

              <v-switch
                v-model="manufacturer.serviceApresVente"
                label="Service Après-Vente"
              ></v-switch>

              <v-btn color="secondary" class="mt-4 mr-2" @click="go_back">
                Retour
              </v-btn>
              <v-btn type="submit" color="primary" class="mt-4" :disabled="!is_form_valid">
                Ajouter le fabricant
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  setup() {
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    const manufacturer = ref({
      nomFabricant: '',
      paysFabricant: '',
      mailFabricant: '',
      numTelephoneFabricant: '',
      serviceApresVente: false
    });
    const error_message = ref('');

    const is_form_valid = computed(() => {
      return manufacturer.value.nomFabricant &&
             manufacturer.value.paysFabricant &&
             manufacturer.value.mailFabricant &&
             manufacturer.value.numTelephoneFabricant &&
             validateEmail(manufacturer.value.mailFabricant);
    });

    const validateEmail = (email) => {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    };

    const submit_form = async () => {
      if (!is_form_valid.value) {
        error_message.value = 'Veuillez remplir tous les champs requis.';
        return;
      }

      error_message.value = ''; // Clear any previous error messages

      try {
        await api.post('fabricants/', manufacturer.value);
        if (true) {
          go_back();
        } else {
          error_message.value = 'Une erreur est survenue lors de la création du fabricant.';
        }
      } catch (error) {
        console.error('Error creating fabricant:', error);
        error_message.value = 'Une erreur est survenue lors de la création du fabricant.';
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    return {
      manufacturer,
      error_message,
      is_form_valid,
      submit_form,
      go_back
    };
  }
};
</script>
