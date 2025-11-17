<template>
  <v-app>
    <v-main>
      <v-container>
        <!-- Filtres et tableau -->
        <v-row>
          <!-- Colonne contenant Liste des défaillances signalées et Liste des interventions terminées -->
          <v-col cols="6">
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">
                Liste des demandes d'interventions
                <v-spacer></v-spacer>
              </v-card-title>
              <v-divider></v-divider>
              <v-data-table
                :headers="failures_headers"
                :items="failures"
                :items-per-page="5"
                :page.sync="failures_page"
                item-value="id"
                class="elevation-1 rounded-lg"
                hide-default-footer
                @click:row="(event, {item}) => open_show_failure(item.id)"
              >
                <template v-slot:item.niveau="{ item }">
                  <v-chip :color="get_level_color(item.niveau)" dark>
                    {{ item.niveau }}
                  </v-chip>
                </template>
              </v-data-table>
              <v-pagination
                v-model="failures_page"
                :length="Math.ceil(failures.length / 5)"
              ></v-pagination>
            </v-card>
          </v-col>

          <v-col cols="6">
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">
                Liste des bons de travail
                <v-spacer></v-spacer>
              </v-card-title>
              <v-divider></v-divider>
              <v-data-table
                :headers="interventions_headers"
                :items="interventions"
                :items-per-page="5"
                :page.sync="interventions_page"
                item-value="id"
                class="elevation-1 rounded-lg"
                hide-default-footer
                @click:row="(event, {item}) => open_show_intervention(item.id)"
              ></v-data-table>
              <v-pagination
                v-model="interventions_page"
                :length="Math.ceil(interventions.length / 5)"
              ></v-pagination>
            </v-card>
          </v-col>
        </v-row>

        <!-- Statistiques -->
        <v-row>
          <v-col cols="4">
            <v-card elevation="1" class="pa-4 text-center">
              <h3>Nombre de demandes d'interventions</h3>
              <p class="display-2">{{ total_failures }}</p>
            </v-card>
          </v-col>
          <v-col cols="4">
            <v-card elevation="1" class="pa-4 text-center">
              <h3>Nombre de bons de travail en cours</h3>
              <p class="display-2">{{ intervention_count }}</p>
            </v-card>
          </v-col>
          <v-col cols="4">
            <v-card elevation="1" class="pa-4 text-center">
              <h3>Répartition des Niveaux</h3>
              <canvas id="levelChart" width="200" height="200"></canvas>
              <div id="chartLegend" class="d-flex justify-space-around mt-4"></div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { getFailureLevelColor } from '@/utils/helpers';
import NavigationDrawer from '@/components/NavigationBar.vue';
import TopNavBar from "@/components/TopBar.vue";
import '@/assets/css/global.css';
import { API_BASE_URL } from '@/utils/constants';

export default {
  components: {
    NavigationDrawer,
    TopNavBar,
  },

  setup() {
    const router = useRouter();
    const failuresApi = useApi(API_BASE_URL);
    const interventionsApi = useApi(API_BASE_URL);

    const open_show_failure = (id) => {
      router.push({ name: 'FailureDetail', params: { id: id } });
    };

    const open_show_intervention = (id) => {
      router.push({ name: 'InterventionDetail', params: { id: id } });
    };

    return {
      open_show_failure,
      open_show_intervention,
      failuresApi,
      interventionsApi
    };
  },

  data() {
    return {
      menu_items: [
        { name: 'Tableau de bord', icon: require('@/assets/images/Graphe.svg') },
        { name: 'Equipements', icon: require('@/assets/images/Outils.svg') },
        { name: 'InterventionList', icon: require('@/assets/images/Maintenance.svg') },
        { name: 'Techniciens', icon: require('@/assets/images/Techniciens.svg') },
      ],
      failures_headers: [
        { title: 'Commentaire', value: 'commentaireDefaillance' },
        { title: 'Niveau', value: 'niveau' },
        { title: 'Équipement', value: 'equipement' },
      ],
      failures: [],
      interventions_headers: [
        { title: 'Nom', value: 'nomIntervention' },
        { title: 'Date d\'assignation', value: 'dateAssignation' },
        { title: 'Temps estimé', value: 'tempsEstime' },
      ],
      interventions: [],
      intervention_count: 0,
      failures_page: 1,
      interventions_page: 1,
      total_failures: 0,
      levelDistribution: [],
    };
  },

  methods: {
    handle_item_selected(item) {
    },

    format_date(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    },

    async fetch_failures() {
      try {
        const response = await this.failuresApi.get('defaillances/');
        this.failures = response.filter(defaillance => defaillance.dateTraitementDefaillance === null);
        this.total_failures = this.failures.length;

        // Calculate level distribution
        const levels = this.failures.map(f => f.niveau);
        this.levelDistribution = [
          levels.filter(level => level === 'Critique').length,
          levels.filter(level => level === 'Majeur').length,
          levels.filter(level => level === 'Mineur').length,
        ];

        // Draw the chart
        this.drawLevelChart();
      } catch (error) {
        console.error('Erreur lors de la récupération des défaillances:', error);
      }
    },

    get_level_color: getFailureLevelColor,

    async fetch_interventions() {
      try {
        const response = await this.interventionsApi.get('interventions/');
        this.interventions = response
          .filter(intervention => intervention.dateCloture === null) // Filtre les interventions non clôturées
          .map(intervention => ({
            ...intervention,
            dateAssignation: this.format_date(intervention.dateAssignation)
          }));
        this.intervention_count = this.interventions.length;
      } catch (error) {
        console.error('Erreur lors de la récupération des interventions:', error);
      }
    },

    drawLevelChart() {
      const ctx = document.getElementById('levelChart').getContext('2d');
      const total = this.levelDistribution.reduce((a, b) => a + b, 0);

      const colors = ['#ff0505', '#ff9808', '#16ad09'];
      const labels = ['Critique', 'Majeur', 'Mineur'];
      let startAngle = 0;

      this.levelDistribution.forEach((count, index) => {
        const sliceAngle = (count / total) * 2 * Math.PI;
        ctx.fillStyle = colors[index];
        ctx.beginPath();
        ctx.moveTo(100, 100);
        ctx.arc(100, 100, 100, startAngle, startAngle + sliceAngle);
        ctx.closePath();
        ctx.fill();
        startAngle += sliceAngle;
      });

      // Draw the legend
      const legendContainer = document.getElementById('chartLegend');
      legendContainer.innerHTML = '';
      labels.forEach((label, index) => {
        const legendItem = document.createElement('div');
        legendItem.style.display = 'flex';
        legendItem.style.alignItems = 'center';
        legendItem.style.marginRight = '20px';

        const colorBox = document.createElement('div');
        colorBox.style.width = '20px';
        colorBox.style.height = '20px';
        colorBox.style.backgroundColor = colors[index];
        colorBox.style.marginRight = '10px';

        const labelText = document.createElement('span');
        labelText.textContent = label;

        legendItem.appendChild(colorBox);
        legendItem.appendChild(labelText);
        legendContainer.appendChild(legendItem);
      });
    }
  },

  created() {
    this.fetch_failures();
    this.fetch_interventions();
  },
};
</script>
