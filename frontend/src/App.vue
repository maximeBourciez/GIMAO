<template>
  <v-app>
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
    
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Sidebar from "@/components/SideBar.vue";
import TopBar from "@/components/TopBar.vue";

export default {
  name: 'App',
  components: {
    Sidebar,
    TopBar,
  },
  
  data() {
    return {
      isMobile: false,
    };
  },
  
  computed: {
    pageTitle() {
      return this.$route.meta?.title || 'GIMAO';
    }
  },
  
  mounted() {
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
  }
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
.v-btn {
  background-color: #F1F5FF;
  border-radius: 50%;
}
h1 {
  color: #05004E;
}
</style>