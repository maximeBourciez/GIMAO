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
              <FormField class="mb-4"
                v-model="nomUtilisateur" 
                label="Nom d'utilisateur" 
                type="text" 
                required 
              />

              <FormField class="mb-4"
                v-if="showPasswordField" 
                v-model="motDePasse" 
                label="Mot de passe" 
                type="password" 
                required 
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

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'
import FormField from '@/components/Forms/inputType/FormField.vue'

const router = useRouter()
const store = useStore()
const api = useApi(API_BASE_URL)

const showPasswordField = ref(false)

const nomUtilisateur = ref('')
const motDePasse = ref('')
const error = ref('')
const loading = ref(false)

const login = async () => {
  error.value = ''
  loading.value = true

  if(showPasswordField.value){
    loginWithPassword()
  }else  { // Vérifier l'existence de l'utilisateur
    checkUserExistence()
  }
}

const loginWithPassword = async () => {
  try {
    const response = await api.post('utilisateurs/login/', {
      nomUtilisateur: nomUtilisateur.value,
      motDePasse: motDePasse.value
    })

    // Si besoin de définir le mot de passe
    if (response.besoinDefinirMotDePasse) {
      router.push({
        name: 'SetPassword',
        query: { username: nomUtilisateur.value }
      })
      return
    }

    // Connexion réussie
    localStorage.setItem('user', JSON.stringify(response.utilisateur))
    store.commit('setUser', response.utilisateur)
    router.push('/')

  } catch (err) {
    if (err.response?.detail) {
      error.value = err.response.detail
    } else {
      error.value = 'Erreur de connexion'
    }
  } finally {
    loading.value = false
  }
}

const checkUserExistence = async () => {
  try {
      const response = await api.post('utilisateurs/exists/', {
        nomUtilisateur: nomUtilisateur.value
      })

      if (response.existe) {
        showPasswordField.value = true
        loading.value = false
      } else {
        router.push({
          name: 'SetPassword',
          query: { username: nomUtilisateur.value }
        })
      }
    } catch (err) {
      error.value = 'Erreur de connexion'
      loading.value = false
    }
}

</script>
