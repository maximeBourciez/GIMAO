<template>
  <v-app-bar app color="white" elevation="2" density="comfortable" class="px-6">
    <!-- Logo and Title -->
    <link rel="icon" href="<%= BASE_URL %>favicon.ico">
    <v-col class="d-flex align-center justify-start">
    </v-col>
    <!-- Left-aligned Page Title -->
    <div class="text-h5 font-weight-bold page_title">
      {{ page_title }}
    </div>

    <v-spacer></v-spacer>

    <!-- Action Buttons -->
    <v-btn
      color="primary"
      class="mr-4 text-none"
      density="comfortable"
      @click="export_database"
    >
      <v-icon start>mdi-database-export</v-icon>
      Exporter la base de données
    </v-btn>

    <v-btn
      color="primary"
      class="mr-4 text-none"
      density="comfortable"
      @click="logout"
    >
      <v-icon start>mdi-logout</v-icon>
      Déconnexion
    </v-btn>

    <!-- Profile Section -->
    <v-avatar size="40" class="ml-4">
      <v-img :src="user_avatar_url" :alt="user_name" cover class="border"></v-img>
    </v-avatar>
    <div class="ml-2 text-left">
      <div class="font-weight-bold user_name">
        {{ user_name }}
      </div>
      <div class="text-caption text-grey-darken-1">
        {{ user_role }}
      </div>
    </div>
  </v-app-bar>
</template>

<script>
export default {
  name: "TopBar",
  props: {
    page_title: {
      type: String,
      required: true
    },
    user_name: {
      type: String,
      default: "Admin"
    },
    user_role: {
      type: String,
      default: "Administrateur"
    },
    user_avatar_url: {
      type: String,
      default: "https://i.imghippo.com/files/SRJI2293jtI.png"
    },
    logo_url: {
      type: String,
      default: "https://i.imghippo.com/files/wCa5810fAA.png"
    }
  },
  methods: {
    export_database() {
    },
    logout() {
    }
  }
};
</script>

<style scoped>
.app_title, .page_title, .user_name {
  color: #151d48;
}

.app_title {
  font-family: 'Montserrat', sans-serif;
}
</style>