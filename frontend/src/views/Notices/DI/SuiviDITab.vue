<template>
    <v-container class="doc-page">
        <h4>
            Consulter vos demandes d’intervention
        </h4>

        <div class="text-body-2 mb-4">
            Dans la liste « Vos DI », vous retrouvez l’ensemble des Demandes d’Intervention que vous avez créées.
            Elle regroupe toutes les défaillances que vous avez signalées par le passé et vous permet de les consulter à tout moment.
            Cette liste vous aide également à suivre l’état d’avancement de vos demandes afin, si nécessaire, de les
            compléter ou de les modifier.

            <ZoomImage :src="require('@/assets/images/notices/Dashboard/opérateur.png')" v-if="role === 'Opérateur'" />
            <!-- <ZoomImage :src="require('@/assets/images/notices/DI/liste-di.png')" v-else/> -->

            <br /><br />

            Les Demandes d’Intervention peuvent apparaître sous différents statuts.

            <br />

             - <strong>En attente</strong> : la DI n’a pas encore été traitée par votre Responsable GMAO.

            <br />

             - <strong>Acceptée</strong> : la DI a été validée par votre responsable et est en attente d’un diagnostic par un technicien.

            <br />

             - <strong>Transformée</strong> : un technicien est intervenu et a estimé qu’une réparation était nécessaire.
            La DI a alors été transformée en Bon de Travail afin de permettre la prise en charge de l’intervention.

            <br />

             - <strong>Refusée</strong> : la DI a été examinée par votre responsable, qui a estimé que la défaillance ne nécessitait pas
            d’intervention.
        </div>

        <!-- Image de la liste des DI -->
        <ZoomImage src="assets/images/notices/liste-di.png" alt="Liste des DI" /> 
    </v-container>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";

const props = defineProps({
    role: {
        type: String,
        default: "Opérateur"
    }
});

const roles = ["Opérateur", "Technicien", "Responsable GMAO0"]

const roleIsAbove = (role) => {
    return roles.indexOf(props.role) >= roles.indexOf(role);
}
</script>