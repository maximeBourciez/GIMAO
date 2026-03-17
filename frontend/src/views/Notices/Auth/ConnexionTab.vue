<template>
    <v-expansion-panels multiple variant="accordion">

        <!-- 🔹 CONNEXION -->
        <v-expansion-panel>
            <v-expansion-panel-title>
                Connexion à l’application
            </v-expansion-panel-title>

            <v-expansion-panel-text>
                <div class="text-body-2 mb-4">
                    <strong>Accéder à l’application :</strong><br /><br />

                    1. Ouvrez votre navigateur web<br />
                    2. Saisissez l’adresse suivante : <strong>http://51.91.252.46</strong><br />
                    3. Sur la page de connexion :<br />
                    &nbsp;&nbsp;• Entrez votre nom d’utilisateur fourni par le responsable GMAO<br />
                    &nbsp;&nbsp;• Cliquez sur <strong>Se connecter</strong>
                </div>

                <ZoomImage src="/images/login.png" alt="Page de connexion" />

                <div class="text-body-2 mb-4">
                    <strong>Première connexion :</strong><br /><br />
                    Lors de votre première connexion, vous devrez définir un mot de passe afin de sécuriser votre
                    compte.
                </div>

                <div class="text-body-2 mb-4">
                    <strong>Connexion classique :</strong><br /><br />
                    Si un mot de passe est déjà défini :<br />
                    &nbsp;&nbsp;• Un champ mot de passe apparaît après avoir cliqué sur <strong>Se
                        connecter</strong><br />
                    &nbsp;&nbsp;• Saisissez votre mot de passe<br />
                    &nbsp;&nbsp;• Cliquez à nouveau sur <strong>Se connecter</strong>
                </div>

                <div class="text-body-2">
                    Une fois connecté, vous accédez à votre <strong>tableau de bord</strong>, adapté à votre rôle.
                </div>
            </v-expansion-panel-text>
        </v-expansion-panel>

        <!-- 🔹 DÉCONNEXION -->
        <v-expansion-panel>
            <v-expansion-panel-title>
                Déconnexion
            </v-expansion-panel-title>

            <v-expansion-panel-text>
                <div class="text-body-2">
                    Si vous souhaitez vous déconnecter :
                    <br /><br />
                    • Revenez au tableau de bord via le fil d’Ariane en haut de l’écran<br />
                    • Cliquez sur <strong>Tableau de bord</strong><br />
                    • En bas à gauche, cliquez sur le bouton <strong>Déconnexion</strong><br /><br />

                    Vous serez alors automatiquement déconnecté de l’application.
                </div>

                <ZoomImage src="/images/logout.png" alt="Bouton déconnexion" />
            </v-expansion-panel-text>
        </v-expansion-panel>

    </v-expansion-panels>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>