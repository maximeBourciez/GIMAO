<template>
  <v-data-table
    :headers="headers"
    :items="documents"
    class="elevation-1 document-table"
    hide-default-footer
    :items-per-page="-1"
  >
    <template #item.name="{ item }">
      <div style="word-wrap: break-word; white-space: normal;">
        {{ item.titre }}
      </div>
    </template>
    
    <template #item.type="{ item }">
      {{ item.type_nom }}
    </template>
    
    <template #item.actions="{ item }">
      <div class="text-no-wrap">
        <v-btn
          icon
          size="small"
          color="primary"
          class="mr-2"
          @click="$emit('download', item)"
          :disabled="downloading"
        >
          <v-icon>mdi-download</v-icon>
        </v-btn>
        
        <v-btn
          icon
          size="small"
          color="error"
          @click="$emit('delete', item)"
          :disabled="deleting"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </div>
    </template>
    
    <template #no-data>
      <div class="text-center pa-4">
        <v-icon size="48" color="grey-lighten-1">mdi-file-document-outline</v-icon>
        <p class="text-grey mt-2">Aucun document</p>
      </div>
    </template>
  </v-data-table>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  documents: {
    type: Array,
    default: () => []
  },
  showType: {
    type: Boolean,
    default: false
  },
  downloading: {
    type: Boolean,
    default: false
  },
  deleting: {
    type: Boolean,
    default: false
  }
});

defineEmits(['download', 'delete']);

const headers = computed(() => {
  const baseHeaders = [
    { title: 'Nom du document', key: 'name' }
  ];
  
  if (props.showType) {
    baseHeaders.push({ title: 'Type', key: 'type' });
  }
  
  baseHeaders.push({ title: 'Actions', key: 'actions' });
  
  return baseHeaders;
});
</script>

<style scoped>
.document-table :deep(table) {
  table-layout: fixed;
  width: 100%;
}

.document-table :deep(.v-data-table__wrapper) {
  overflow-x: hidden !important;
}

.document-table :deep(td:first-child),
.document-table :deep(th:first-child) {
  width: auto !important;
}

.document-table :deep(td:nth-child(2)),
.document-table :deep(th:nth-child(2)) {
  width: 150px !important;
}

.document-table :deep(td:last-child),
.document-table :deep(th:last-child) {
  width: 120px !important;
  text-align: center;
}
</style>
