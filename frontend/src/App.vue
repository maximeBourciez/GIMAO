<template>
  <v-app>
    <!-- N'afficher la navigation que si on n'est pas sur une page publique -->
    <template v-if="!isPublicPage">
      <!-- Desktop Sidebar -->
      <Sidebar v-if="!isMobile" />
      
      <!-- Mobile TopBar (avec menu hamburger) -->
      <TopBar v-if="isMobile" />
      
      <!-- Desktop TopBar (juste le titre, pas de hamburger) -->
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
  </v-app>
</template>

<script>
import Sidebar from "@/components/SideBar.vue";
import TopBar from "@/components/TopBar.vue";
import Breadcrumb from "@/components/Breadcrumb.vue";

export default {
  name: 'App',
  components: {
    Sidebar,
    TopBar,
    Breadcrumb
  },
  
  data() {
    return {
      isMobile: false,
    };
  },
  
  computed: {
    pageTitle() {
      return this.$route.meta?.title || 'GIMAO';
    },
    isPublicPage() {
      return this.$route.meta?.public === true;
    }
  },
  
  mounted() {
    // Initialiser l'authentification depuis le localStorage
    this.$store.dispatch('initAuth');
    
    this.checkIfMobile();
    window.addEventListener('resize', this.checkIfMobile);
  },
  
  beforeUnmount() {
    window.removeEventListener('resize', this.checkIfMobile);
  },
  
  methods: {
    checkIfMobile() {
      this.isMobile = window.innerWidth < 960; // Breakpoint md de Vuetify
    }
  },

};
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
h1 {
  color: #05004E;
}
</style>