<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card elevation="1" class="rounded-lg pa-2">
              <h1 class="text-primary text-center mb-4">Demande d'intervention</h1>
              <v-row>
                <v-col cols="6">
                  <v-row>
                    <v-col cols="12">
                      <p class="mb-4"><strong>Equipement:</strong> {{ recovered_information.designation }}</p>
                    </v-col>
                    <v-col cols="12">
                      <p class="mb-4"><strong>Salle:</strong> {{ recovered_information.nomLieu }}</p>
                    </v-col>
                    <v-col cols="12">
                      <p class="mb-4">
                        <v-row justify="start">
                          <v-col cols="auto">
                            <strong>Etat de la machine :</strong>
                            <v-chip :color="get_level_color(recovered_information.statutEquipement)" dark>
                              {{ recovered_information.statutEquipement }}
                            </v-chip>
                          </v-col>
                        </v-row>
                      </p>
                    </v-col>
                  </v-row>
                </v-col>

                <!-- Colonne de droite qui contient le champ commentaire -->
                <v-col cols="6">
                  <p><strong>Informations sur la défaillance</strong></p>
                  <p>{{ recovered_information.commentaireDefaillance }}</p>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>

        <v-container>
          <v-row>
            <v-col cols="12">
              <v-card elevation="1" class="rounded-lg pa-2">
                <h2 class="text-primary text-center mb-4">Informations du bon de travail</h2>

                <!-- Error Alert -->
                <v-alert v-if="error_message" type="error" class="mb-4">
                  {{ error_message }}
                </v-alert>

                <v-form ref="formulaire" v-model="valid_form" @submit.prevent="validate_form">
                  <v-row>
                    <v-col cols="6">
                      <p class="mb-4"><strong>Nom du bon de travail</strong></p>
                      <v-text-field
                        v-model="form.intervention_name"
                        label="Nom du bon de travail"
                        type="text"
                        outlined
                        dense
                        :rules="[v => !!v || 'Nom du bon de travail requis']"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="6">
                      <p class="mb-4"><strong>Date de début d'intervention</strong></p>
                      <v-text-field
                        v-model="form.start_date"
                        type="datetime-local"
                        outlined
                        dense
                        :rules="[v => !!v || 'Date de début requise']"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="6">
                      <p class="mb-4"><strong>Intervention curative</strong></p>
                      <v-switch
                        v-model="form.curative_intervention"
                        label="Intervention Curative"
                        color="primary"
                        hide-details
                        inset
                      ></v-switch>
                    </v-col>

                    <v-col cols="6">
                      <p class="mb-4"><strong>Temps estimé (en heures)</strong></p>
                      <v-text-field
                        v-model="form.estimated_time"
                        label="Temps estimé (facultatif)"
                        type="number"
                        outlined
                        dense
                        min="0"
                        step="1"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="6">
                    </v-col>
                    <v-col cols="6"></v-col>

                    <v-row justify="center">
                      <v-col cols="10">
                        <v-row justify="center">
                          <p class="mb-4"><strong>Commentaire</strong></p>
                        </v-row>
                        <v-textarea
                          v-model="form.comment_to_fill_in"
                          rows="10"
                          outlined
                          :rules="[v => !!v || 'Commentaire requis']"
                        ></v-textarea>
                      </v-col>
                    </v-row>
                  </v-row>
                </v-form>
              </v-card>
            </v-col>
          </v-row>

          <v-row justify="center" class="mt-4">
            <v-btn color="primary" class="text-white mx-2" @click="back_to_previous_page">
              Annuler
            </v-btn>
            <v-btn color="success" class="text-white mx-2" @click="validate_form">
              Valider
            </v-btn>
          </v-row>
        </v-container>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import '@/assets/css/global.css';
import { reactive, onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';

export default {
  name: 'CreateIntervention',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const error_message = ref(''); // Add error message

    const get_level_color = (niveau) => {
      switch (niveau) {
        case 'À l\'arrêt':
          return 'red';
        case 'Majeur':
          return 'orange';
        default:
          return 'green';
      }
    };

    const recovered_information = reactive({
      designation: "",
      nomLieu: "",
      commentaireDefaillance: "",
      statutEquipement: "",
    });

    const form = reactive({
      intervention_name: "",
      start_date: "",
      technicien: "",
      curative_intervention: false,
      estimated_time: null,
      createurIntervention: 1,
      comment_to_fill_in: "",
    });

    const technicians = ref([]);
    const curative_intervention = [
      { text: 'Oui', value: true },
      { text: 'Non', value: false }
    ];

    const valid_form = ref(false);

    const fetch_data = async () => {
      try {
        const failure_id = route.params.id;
        if (!failure_id) {
          throw new Error('ID de défaillance manquant');
        }

        const [failure_res, users_res] = await Promise.all([
          api.getDefaillanceAffichage(failure_id),
          api.getUtilisateur()
        ]);

        if (failure_res && failure_res.data) {
          Object.assign(recovered_information, {
            designation: failure_res.data.equipement.designation,
            nomLieu: failure_res.data.equipement.lieu.nomLieu,
            commentaireDefaillance: failure_res.data.commentaireDefaillance,
            statutEquipement: failure_res.data.equipement.dernier_statut.statutEquipement
          });
        } else {
          console.error('Aucune donnée de défaillance reçue de l\'API');
        }

        if (users_res && users_res.data) {
          technicians.value = users_res.data
            .filter(user => user.role === 'Technicien')
            .map(tech => ({
              text: `${tech.prenom} ${tech.nom}`,
              value: tech.id
            }));
        } else {
          console.error('Aucune donnée d\'utilisateurs reçue de l\'API');
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des données:', error);
        error_message.value = 'Erreur lors de la récupération des données. Veuillez réessayer.';
      }
    };

    const back_to_previous_page = () => {
      router.go(-1);
    };

    const delete_intervention_request = () => {
      router.push({ name: 'Dashboard' });
    };

    const validate_form = async () => {
      if (valid_form.value) {
        try {
          const interventionData = {
            nomIntervention: form.intervention_name,
            interventionCurative: form.curative_intervention,
            dateAssignation: new Date().toISOString(),
            dateCloture: null,
            dateDebutIntervention: form.start_date,
            dateFinIntervention: null,
            tempsEstime: form.estimated_time ? `${form.estimated_time.toString().padStart(2, '0')}:00:00` : null,
            commentaireIntervention: form.comment_to_fill_in,
            commentaireRefusCloture: null,
            defaillance: parseInt(route.params.id),
            createurIntervention: 1,
            responsable: 1
          };

          const response = await api.postIntervention(interventionData);

          if (response && response.data) {
            // Redirection vers la page d'affichage de l'intervention
            router.push({ name: 'Dashboard' });
          } else {
            throw new Error('Réponse invalide du serveur');
          }
        } catch (error) {
          console.error('Erreur lors de la création de l\'intervention:', error);
          error_message.value = "Erreur lors de la création de l'intervention. Veuillez réessayer.";
        }
      } else {
        error_message.value = "Le formulaire n'est pas complet. Veuillez remplir les champs obligatoires.";
      }
    };

    onMounted(fetch_data);

    return {
      form,
      recovered_information,
      technicians,
      curative_intervention,
      valid_form,
      back_to_previous_page,
      delete_intervention_request,
      validate_form,
      get_level_color,
      error_message, // Return error message
      menuItems: [
        { title: 'Tableau de bord', icon: 'mdi-view-dashboard', route: '/tableau-de-bord' },
        { title: 'Interventions', icon: 'mdi-wrench', route: '/interventions' },
        { title: 'Equipements', icon: 'mdi-laptop', route: '/equipements' },
        { title: 'Gestion des données', icon: 'mdi-database', route: '/gestion-donnees' },
        { title: 'Commandes', icon: 'mdi-cart', route: '/commandes' },
      ],
      handle_item_selected(route) {
        router.push(route);
      },
    };
  },
};
</script>

<style scoped>
/* Ajoutez ici vos styles spécifiques si nécessaire */
</style>
