<template>
    <v-container class="doc-page">
        <h4>
            Modifier une demande d’intervention
        </h4>

        <div class="text-body-2 mb-4">
            Quand vous avez créé une demande d'intervention, celle-ci apparaît sur votre tableau de bord. Si vous
            souhaitez la modifier, il suffit de cliquer dessus. Une fois cela fait, vous arriverez sur la page des
            détails de votre DI, page sur laquelle vous pourrez modifier les informations relatives à votre demande
            d'intervention à l'aide du petit bouton 'Stylo' Situé en bas à droite de votre écran.
        </div>

        <!-- <ZoomImage src="/images/edit-di.png" alt="Modification DI" /> -->

        <div class="text-body-2 mb-4">
            Vous pouvez ensuite modifier les informations de votre demande d'intervention à votre guise, puis en
            cliquant sur 'Enregistrer les modifications', vous serez redirigé vers les détails de votre DI modifiée.
        </div>

        <ZoomImage src="@/assets/images/di-list.png" alt="Liste des DI" />
    </v-container>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>