<template>
  <v-container class="py-6">
    <v-btn
      :style="{ position: 'fixed', top: '80px', left: '16px', zIndex: 2500 }"
      color="secondary"
      variant="tonal"
      icon="mdi-arrow-left"
      aria-label="Retour"
      @click="goBack"
    />

    <v-row>
      <v-col cols="12">
        <v-card elevation="1" class="pa-4">
          <div class="text-h5 font-weight-bold mb-2">Notices d'utilisation</div>
          <div class="text-body-2 text-medium-emphasis">
            Ces notices servent de guide rapide. Elles sont organisées par rôle.
          </div>

          <v-divider class="my-4" />

          <v-tabs v-model="tab" density="comfortable" color="primary">
            <v-tab value="global">Global</v-tab>
            <v-tab value="operateur">Opérateur</v-tab>
            <v-tab value="technicien">Technicien</v-tab>
            <v-tab value="magasinier">Magasinier</v-tab>
            <v-tab value="responsable">Responsable</v-tab>
          </v-tabs>

          <v-divider class="mb-4" />

          <v-window v-model="tab">
            <v-window-item value="global">
              <NoticeGlobale />
            </v-window-item>
            <v-window-item value="operateur">
              <NoticeOperateur />
            </v-window-item>
            <v-window-item value="technicien">
              <NoticeTechnicien />
            </v-window-item>
            <v-window-item value="magasinier">
              <NoticeMagasinier />
            </v-window-item>
            <v-window-item value="responsable">
              <NoticeResponsable />
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import NoticeGlobale from '@/views/Notices/NoticeGlobale.vue'
import NoticeOperateur from '@/views/Notices/NoticeOperateur.vue'
import NoticeTechnicien from '@/views/Notices/NoticeTechnicien.vue'
import NoticeMagasinier from '@/views/Notices/NoticeMagasinier.vue'
import NoticeResponsable from '@/views/Notices/NoticeResponsable.vue'

const tab = ref('global')

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
    return
  }
  router.push('/')
}
</script>
