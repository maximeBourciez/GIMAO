<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card v-if="modelEquipment">
          <v-card-title>Détails du modèle équipement</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Nom du modèle équipement</v-list-item-title>
                  <v-list-item-subtitle>{{ modelEquipment.nomModeleEquipement }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Fabricant</v-list-item-title>
                  <v-list-item-subtitle>{{ manufacturer_name }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        <v-alert v-else type="error">Modèle Equipement non trouvé</v-alert>
        <v-btn color="primary" class="mt-4" @click="go_back">Retour</v-btn>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import api from '@/services/api';
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'ModelEquipmentDetail',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const modelEquipment = ref(null);
    const manufacturer = ref(null);

    const manufacturer_name = computed(() => {
      return manufacturer.value ? manufacturer.value.nomFabricant : 'Non spécifié';
    });

    const fetch_modelEquipment = async () => {
      try {
        const response = await api.getModeleEquipement(route.params.id);
        modelEquipment.value = response.data;
        if (modelEquipment.value.fabricant) {
          await get_manufacturer(modelEquipment.value.fabricant);
        }
      } catch (error) {
        console.error('Error loading the modelEquipment:', error);
      }
    };

    const get_manufacturer = async (id) => {
      try {
        const response = await api.getFabricant(id);
        manufacturer.value = response.data;
      } catch (error) {
        console.error('Error fetching fabricant:', error);
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      fetch_modelEquipment();
    });

    return {
      modelEquipment,
      manufacturer_name,
      go_back,
    };
  },
};
</script>
