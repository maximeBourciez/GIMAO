<template>
  <v-container fluid class="fill-height" style="background: #f5f5f5;">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6" md="4">
        <v-card class="pa-6">
          <v-card-title class="text-center text-h5 mb-4">
            Connexion GIMAO
          </v-card-title>

          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="nomUtilisateur"
                label="Nom d'utilisateur"
                variant="outlined"
                class="mb-3"
              />

              <v-text-field
                v-model="motDePasse"
                label="Mot de passe"
                type="password"
                variant="outlined"
                class="mb-3"
              />

              <v-alert v-if="error" type="error" class="mb-3">
                {{ error }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                :loading="loading"
              >
                Se connecter
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  
  data() {
    return {
      nomUtilisateur: '',
      motDePasse: '',
      error: '',
      loading: false
    }
  },

  methods: {
    async login() {
      this.error = ''
      this.loading = true

      try {
        const response = await axios.post('http://localhost:8000/api/utilisateurs/login/', {
          nomUtilisateur: this.nomUtilisateur,
          motDePasse: this.motDePasse
        })

        // Si besoin de définir le mot de passe
        if (response.data.besoinDefinirMotDePasse) {
          this.$router.push({
            name: 'SetPassword',
            query: { username: this.nomUtilisateur }
          })
          return
        }

        // Connexion réussie
        localStorage.setItem('user', JSON.stringify(response.data.utilisateur))
        this.$store.commit('setUser', response.data.utilisateur)
        this.$router.push('/')

      } catch (err) {
        if (err.response?.data?.detail) {
          this.error = err.response.data.detail
        } else {
          this.error = 'Erreur de connexion'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
