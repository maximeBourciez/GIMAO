<template>
  <v-container class="doc-page">
    <h4>Réaliser et documenter une intervention</h4>

    <div class="text-body-2 mb-4 mt-2">
      En tant que technicien ou responsable, vous êtes chargé d'exécuter les Bons de Travail qui vous sont assignés. Cette section vous permet de mettre à jour le statut de l'intervention et d'y apporter toutes les informations nécessaires à son suivi.
      <br /><br />

      <strong>Informations visibles sur la fiche d'un Bon de Travail :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Colonne de gauche :</strong> vous y trouverez les informations principales telles que le nom, le type (correctif ou préventif), le statut, le diagnostic métier, la date d'assignation, la date de début prévue, la durée prévue, la date de début réelle, la date de fin et la date de clôture.</li>
        <li><strong>Colonne de droite :</strong> elle contient des compléments détaillés :
          <ul class="ml-4 mt-2">
            <li><strong>Commentaires :</strong> commentaire général et commentaire de refus de clôture éventuel.</li>
            <li><strong>Affectation :</strong> le responsable de l'intervention et les utilisateurs assignés.</li>
            <li><strong>Demande d'intervention associée :</strong> nom, commentaire, demandeur et date de création de la DI originale.</li>
            <li><strong>Équipement :</strong> référence, désignation, lieu et statut de l'équipement concerné.</li>
            <li><strong>Documents :</strong> nom, type et boutons pour télécharger ou supprimer les fichiers joints.</li>
            <li><strong>Consommables :</strong> l'image, la désignation et la quantité des pièces demandées pour le BT.</li>
          </ul>
        </li>
      </ul>

      <ZoomImage :src="require('@/assets/images/notices/BT/detail-bt-technicien.png')" alt="Détail du Bon de Travail" v-if="role === 'Technicien'"/>
      <!-- <ZoomImage :src="require('@/assets/images/notices/BT/detail-bt-responsable.png')" alt="Détail du Bon de Travail" v-else/> -->

      <strong>Le cycle de vie d'une intervention :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Démarrer une intervention</strong> : depuis le détail du BT, cliquez sur l'action <strong>Démarrer</strong> lorsque vous commencez physiquement les travaux. Le statut du BT passe alors à <em>En cours</em> et l'heure de début est officiellement enregistrée.</li>
        <li><strong>Terminer une intervention</strong> : une fois les réparations achevées et les équipements remis en fonction, cliquez sur <strong>Terminer</strong>. Le statut passe à <em>Terminé</em> et l'heure de fin est sauvegardée, ce qui permet notamment de calculer le temps passé sur l'intervention.</li>
      </ul>

      <ZoomImage :src="require('@/assets/images/notices/BT/demarrer-bt-technicien.png')" alt="Demarrer l'intervention" v-if="role === 'Technicien'"/>
      <!-- <ZoomImage :src="require('@/assets/images/notices/BT/demarrer-bt-responsable.png')" alt="Demarrer l'intervention" v-else/> -->
      <ZoomImage :src="require('@/assets/images/notices/BT/terminer-bt-technicien.png')" alt="Terminer l'intervention" v-if="role === 'Technicien'"/>
      <!-- <ZoomImage :src="require('@/assets/images/notices/BT/terminer-bt-responsable.png')" alt="Terminer l'intervention" v-else/> -->

      <strong>Documenter l'intervention (Compte-rendu) :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Diagnostic et commentaires :</strong> à tout moment de l'intervention, vous pouvez modifier le compte-rendu du BT pour y consigner votre diagnostic, noter les difficultés rencontrées ou préciser le travail qui a été effectué.</li>
        <li><strong>Pièces jointes :</strong> n'hésitez pas à télécharger des documents pertinents pour clôturer correctement le dossier (photos avant/après, rapport d'intervention constructeur, etc.).</li>
      </ul>

      <strong>Consommation de pièces détachées :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Demander des pièces :</strong> si vous avez besoin de matériel pour l'intervention, vous pouvez en faire la demande via la section "Consommables" de l'intervention. Indiquez la quantité requise et le produit désiré.</li>
        <li><strong>Déduction du stock :</strong> La demande sera évaluée et validée par le magasinier ou le responsable. Une fois validée par ces derniers (ou lors de la clôture), le stock sera automatiquement mis à jour.</li>
      </ul>
    
      <ZoomImage :src="require('@/assets/images/notices/BT/detail-bt-technicien-edit.png')" alt="Modifier le Bon de Travail" v-if="role === 'Technicien'"/>
      <!-- <ZoomImage :src="require('@/assets/images/notices/BT/detail-bt-responsable-edit.png')" alt="Modifier le Bon de Travail" v-else/> -->

      <strong>N'oubliez pas de valider vos modifications avant de quitter la page.</strong>

      <ZoomImage :src="require('@/assets/images/notices/BT/modif-bt-technicien.png')" alt="Valider les modifications du Bon de Travail" v-if="role === 'Technicien'"/>
      <!-- <ZoomImage :src="require('@/assets/images/notices/BT/modif-bt-responsable.png')" alt="Valider les modifications du Bon de Travail" v-else/> -->
      
    </div>
  </v-container>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";

const props = defineProps({
  role: {
    type: String,
    default: "Technicien"
  }
});

const roles = ["Technicien", "Responsable GMAO"];

const roleIsAbove = (minRole) => {
  return roles.indexOf(props.role) >= roles.indexOf(minRole);
};
</script>

<style scoped>
.doc-page {
  padding: 0;
}
ul li {
  margin-bottom: 8px;
}
</style>
