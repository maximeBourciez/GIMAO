<template>
  <v-app>
    <v-main>
      <v-container class="py-5">
        <v-card class="pa-4">
          <v-form ref="form" v-model="form_valid">

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
import { useRouter } from 'vue-router';
import '@/assets/css/global.css';
import api from '@/services/api';

export default {
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      equipment_list: [],
      levels: ['Mineur', 'Majeur', 'Critique'],
      form: {
        equipement: null,
        commentaireDefaillance: "",
        niveau: null,
      },
      form_valid: false,
      validation_triggered: false,
      equipment_reference: null,
      connected_user: {
        id: 1,
        username: "admin",
        first_name: "admin",
        last_name: "admin",
        email: "admin@a.com",
      },
      error_message: "", // Keep error message
    };
  },

  async created() {
    await this.fetch_data();
    this.equipment_reference = this.$route.params.equipementReference;
    if (this.equipment_reference) {
      this.form.equipement = this.equipment_reference;
    }
  },

  methods: {
    async fetch_data() {
      try {
        const [equipments_response] = await Promise.all([
          api.getEquipements(),
        ]);
        this.equipment_list = equipments_response.data.map(eq => ({
          ...eq,
          label: `${eq.reference} - ${eq.designation}`
        }));
      } catch (error) {
        console.error('Erreur lors de la récupération des données:', error);
      }
    },

    reset_form() {
      this.form = {
        equipement: this.equipment_reference || null,
        commentaireDefaillance: "",
        niveau: null,
      };
      this.validation_triggered = false;
      this.error_message = ""; // Clear error message
      if (this.$refs.form) {
        this.$refs.form.resetValidation();
      }
    },

    go_back(){
      this.router.go(-1);
    },

    async validate_form() {
      this.validation_triggered = true;
      const form = this.$refs.form;

      if (form) {
        form.validate();
        if (this.form_valid) {
          try {
            const failure_data = {
              commentaireDefaillance: this.form.commentaireDefaillance,
              niveau: this.form.niveau,
              equipement: this.form.equipement,
              utilisateur: this.connected_user.id,
              dateTraitementDefaillance: null
            };
            const response = await api.postDefaillance(failure_data);

            const new_failure_id = response.data.id;

            // Navigate immediately after successful form submission
            this.router.push({ name: 'FailureDetail', params: { id: new_failure_id } });

          } catch (error) {
            console.error('Erreur lors de la création de la défaillance:', error);
            this.error_message = "Une erreur est survenue lors de la création de la défaillance.";
          }
        } else {
          this.error_message = "Veuillez remplir tous les champs obligatoires.";
        }
      }
    },
  },
};
</script>

