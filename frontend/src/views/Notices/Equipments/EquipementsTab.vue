<template>
  <v-expansion-panels multiple variant="accordion">

    <!-- 🔹 LISTE -->
    <v-expansion-panel>
      <v-expansion-panel-title>
        Liste des équipements
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <EquipmentsListTab />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <!-- 🔹 DÉTAIL -->
    <v-expansion-panel>
      <v-expansion-panel-title>
        Détails d’un équipement
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <EquipmentDetailTab />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <!-- 🔹 DÉFAILLANCE -->
    <v-expansion-panel>
      <v-expansion-panel-title>
        Signaler une défaillance
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <SignalFailureTab />
      </v-expansion-panel-text>
    </v-expansion-panel>

  </v-expansion-panels>
</template>

<script setup>
import EquipmentsListTab from "./EquipmentsListTab.vue";
import EquipmentDetailTab from "./EquipmentDetailTab.vue";
import SignalFailureTab from "./SignalFailureTab.vue";

const props = defineProps({
  role: {
    type: String,
    default: "Opérateur"
  }
});

const roles = ["Opérateur", "Technicien", "Responsable GMAO"];

const roleIsAbove = (minRole) => {
  return roles.indexOf(props.role) >= roles.indexOf(minRole);
};
</script>