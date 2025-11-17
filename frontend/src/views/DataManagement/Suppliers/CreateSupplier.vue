<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Ajouter un nouveau fournisseur</v-card-title>
          <v-card-text>
            <v-alert v-if="error_message" type="error">
              {{ error_message }}
            </v-alert>
            <v-form @submit.prevent="submit_form">
              <v-text-field
                v-model="supplier.nomFournisseur"
                label="Nom du fournisseur"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.numRue"
                label="Numéro de rue"
                type="number"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.nomRue"
                label="Nom de rue"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.codePostal"
                label="Code postal"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.ville"
                label="Ville"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.paysFournisseur"
                label="Pays"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.mailFournisseur"
                label="Email"
                type="email"
                required
              ></v-text-field>

              <v-text-field
                v-model="supplier.numTelephoneFournisseur"
                label="Numéro de téléphone"
                required
              ></v-text-field>

              <v-switch
                v-model="supplier.serviceApresVente"
                label="Service après vente"
              ></v-switch>

              <v-btn color="secondary" class="mt-4 mr-2" @click="go_back">
                Retour
              </v-btn>
              <v-btn type="submit" color="primary" class="mt-4" :disabled="!is_form_valid">
                Ajouter fournisseur
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
import api from '@/services/api';

export default {
  setup() {
    const router = useRouter();
    const supplier = ref({
      nomFournisseur: '',
      numRue: '',
      nomRue: '',
      codePostal: '',
      ville: '',
      paysFournisseur: '',
      mailFournisseur: '',
      numTelephoneFournisseur: '',
      serviceApresVente: false
    });
    const error_message = ref('');

    const is_form_valid = computed(() => {
      return supplier.value.nomFournisseur &&
             supplier.value.numRue &&
             supplier.value.nomRue &&
             supplier.value.codePostal &&
             supplier.value.ville &&
             supplier.value.paysFournisseur &&
             supplier.value.mailFournisseur &&
             supplier.value.numTelephoneFournisseur;
    });

    const submit_form = async () => {
      if (!is_form_valid.value) {
        error_message.value = 'Veuillez remplir tous les champs requis.';
        return;
      }

      try {
        const response = await api.postFournisseur(supplier.value);
        go_back();
      } catch (error) {
        console.error('Error creating supplier:', error);
        error_message.value = "Une erreur est survenue lors de l'ajout du fournisseur.";
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    return {
      supplier,
      error_message,
      is_form_valid,
      submit_form,
      go_back
    };
  }
};
</script>
