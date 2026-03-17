<template>
    <v-container class="doc-page">
        <h4>
            Modifier une demande d’intervention
        </h4>

        <div class="text-body-2 mb-4">
            Une fois votre Demande d’Intervention créée, elle apparaît sur votre tableau de bord.
            Si vous souhaitez la modifier, il vous suffit de cliquer dessus afin d’accéder à sa page de détails.

            Depuis cette page, vous pouvez modifier les informations de votre demande à l’aide du bouton « Stylo »,
            situé en bas à droite de l’écran.

            
        </div>

        <ZoomImage src="/images/edit-di.png" alt="Modification DI" /> 

        <div class="text-body-2 mb-4">
            Après avoir effectué vos modifications, cliquez sur « Enregistrer les modifications ». Vous serez alors
            redirigé vers la page de détails mise à jour de votre DI.
        </div>

    </v-container>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>