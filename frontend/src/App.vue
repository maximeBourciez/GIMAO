<template>
  <v-app>

    <!-- Navigation (si page privée ET utilisateur a menu) -->
    <template v-if="!isPublicPage && userHasMenu  && !isNoticePage">

      <!-- Sidebar desktop -->
      <Sidebar v-if="!isMobile" />

      <!-- TopBar mobile (hamburger) -->
      <TopBar v-if="isMobile" />

      <!-- AppBar desktop -->
      <v-app-bar v-if="!isMobile" app color="white" elevation="1">
        <v-toolbar-title class="font-weight-bold ml-4">
          {{ pageTitle }}
        </v-toolbar-title>
      </v-app-bar>

    </template>

    <v-main>
      <Breadcrumb v-if="!isPublicPage" />
      <router-view />
    </v-main>

    <v-btn
      v-if="isNoticePage"
      :style="{ position: 'fixed', top: '72px', right: '16px', zIndex: 2500 }"
      color="secondary"
      icon="mdi-arrow-left"
      elevation="6"
      aria-label="Retour"
      @click="router.back()"
    />
    <v-btn
      v-else
      :style="{ position: 'fixed', top: '72px', right: '16px', zIndex: 2500 }"
      color="primary"
      icon="mdi-help"
      elevation="6"
      aria-label="Ouvrir les notices d'utilisation"
      @click="goToNotices"
    />

  </v-app>
</template>


<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

import Sidebar from '@/components/SideBar.vue'
import TopBar from '@/components/TopBar.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'

const store = useStore()
const route = useRoute()
const router = useRouter()

/**
 * Mobile
 */
const isMobile = ref(false)

const checkIfMobile = () => {
  isMobile.value = window.innerWidth < 960 // breakpoint md Vuetify
}

/**
 * Auth / rôles
 */
const userRole = computed(() => store.getters.userRole)

const userHasMenu = computed(() => {
  return store.getters.userPermissions.includes('menu:view')
})

/**
 * Pages publiques
 */
const isPublicPage = computed(() => route.meta?.public === true)

/**
 * Titre page
 */
const pageTitle = computed(() => route.meta?.title || 'GIMAO')

const isNoticePage = computed(() => route.name === 'Notice')

const goToNotices = () => {
  router.push('/Notice')
}

/**
 * Lifecycle
 */
onMounted(() => {
  store.dispatch('initAuth')

  checkIfMobile()
  window.addEventListener('resize', checkIfMobile)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkIfMobile)
})
</script>
<style>
.text-primary {
  color: #05004E;
}

.text-dark {
  color: #3C3C3C;
}

.v-card {
  background-color: #FFFFFF;
}

.v-btn {
  background-color: #F1F5FF;
  border-radius: 50%;
}

h1 {
  color: #05004E;
}
</style>
