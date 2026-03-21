<template>
    <v-expansion-panels multiple variant="accordion" class="doc-page">

        <!-- CONNEXION -->
        <v-expansion-panel>
            <v-expansion-panel-title>
                Connexion à l'application
            </v-expansion-panel-title>

            <v-expansion-panel-text>
                <div class="text-body-2 mb-4">
                    <strong>Accéder à l'application :</strong><br /><br />

                    Sur la page de connexion :<br />
                    - Entrez votre nom d'utilisateur fourni par le responsable GMAO<br />
                    - Cliquez sur <strong>Se connecter</strong>
                </div>

                <ZoomImage :src="require('@/assets/images/notices/auth/login-1.png')" alt="Page de connexion" />

                <div class="text-body-2 mb-4">
                    <strong>Première connexion :</strong><br /><br />
                    Lors de votre première connexion, vous devrez définir un mot de passe afin de sécuriser votre
                    compte.
                </div>

                <ZoomImage :src="require('@/assets/images/notices/auth/login-3.png')" alt="Définition du mot de passe" />

                <v-divider class="my-4" />

                <div class="text-body-2 mb-4">
                    <strong>Connexion classique :</strong><br /><br />
                    Si un mot de passe est déjà défini :<br />
                    - Un champ mot de passe apparaît après avoir cliqué sur <strong>Se
                        connecter</strong><br />
                    - Saisissez votre mot de passe<br />
                    - Cliquez à nouveau sur <strong>Se connecter</strong>
                </div>

                <ZoomImage :src="require('@/assets/images/notices/auth/login-2.png')" alt="Connexion classique" />

                <div class="text-body-2">
                    Une fois connecté, vous accédez à votre <strong>tableau de bord</strong>, adapté à votre rôle.
                </div>
            </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- DÉCONNEXION -->
        <v-expansion-panel>
            <v-expansion-panel-title>
                Déconnexion
            </v-expansion-panel-title>

            <v-expansion-panel-text>
                <div class="text-body-2">
                    Si vous souhaitez vous déconnecter :
                    <br /><br />
                    - Revenez au tableau de bord via le fil d'Ariane en haut de l'écran<br />
                    - Cliquez sur <strong>Tableau de bord</strong><br />
                    - En bas à gauche, cliquez sur le bouton <strong>Déconnexion</strong><br /><br />

                    Vous serez alors automatiquement déconnecté de l'application.
                </div>

                <ZoomImage :src="require('@/assets/images/notices/auth/logout-opérateur.png')" alt="Bouton déconnexion" v-if="!hasMenu"/>
                <ZoomImage :src="require('@/assets/images/notices/auth/logout-technicien.png')" alt="Bouton déconnexion" v-else/>
            </v-expansion-panel-text>
        </v-expansion-panel>

    </v-expansion-panels>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";

const props = defineProps({
    hasMenu: {
        type: Boolean,
        default: false
    }
});
</script>

<style scoped>
.doc-page {
  max-width: 80%;
  margin: auto;
  margin-bottom: 2rem;
}
</style>