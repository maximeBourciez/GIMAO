<template>
    <v-container class="doc-page">
        <h4>
            Modifier une demande d'intervention
        </h4>

        <div class="text-body-2 mb-4" v-if="role === 'Opérateur'">
            Une fois votre Demande d'Intervention créée, elle apparaît sur votre tableau de bord.
            Si vous souhaitez la modifier, il vous suffit de cliquer dessus afin d'accéder à sa page de détails.

            Depuis cette page, vous pouvez modifier les informations de votre demande à l'aide du bouton « Stylo »,
            situé en bas à droite de l'écran.
        </div>
        <div class="text-body-2 mb-4" v-else>
            Les Demandes d'Intervention sont consultables dans le menu correspondant.
            Si vous souhaitez en modifier une pour compléter les informations (statut, priorité, etc.), cliquez sur la ligne
            souhaitée pour accéder à sa page de détails.

            Depuis cette page, vous pouvez modifier les informations de la demande à l'aide du bouton « Stylo »,
            situé en bas à droite de l'écran.
        </div>

        <ZoomImage :src="require('@/assets/images/notices/DI/detail-di-edit.png')" alt="Modification DI" v-if="role === 'Opérateur'"/>
        <ZoomImage :src="require('@/assets/images/notices/DI/detail-di-technicien-edit.png')" alt="Modification DI" v-else/> 

        <div class="text-body-2 mb-4">
            Après avoir effectué vos modifications, cliquez sur « Enregistrer les modifications ». Vous serez alors
            redirigé vers la page de détails mise à jour de votre DI.
        </div>
        
        <ZoomImage :src="require('@/assets/images/notices/DI/modif-di.png')" alt="Modification DI" v-if="role === 'Opérateur'"/> 
        <ZoomImage :src="require('@/assets/images/notices/DI/modif-di-technicien.png')" alt="Modification DI" v-else/> 

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

const roles = ["Opérateur", "Technicien", "Responsable GMAO"];

const roleIsAbove = (minRole) => {
  return roles.indexOf(props.role) >= roles.indexOf(minRole);
};
</script>