<template>
  <v-container class="doc-page">
    <h4>Réaliser et documenter une intervention</h4>

    <div class="text-body-2 mb-4 mt-2">
      En tant que technicien ou responsable, vous êtes chargé d'exécuter les Bons de Travail qui vous sont assignés. Cette section vous permet de mettre à jour le statut de l'intervention et d'y apporter toutes les informations nécessaires à son suivi.
      <br /><br />

      <strong>Le cycle de vie d'une intervention :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Démarrer une intervention</strong> : depuis le détail du BT, cliquez sur l'action <strong>Démarrer</strong> lorsque vous commencez physiquement les travaux. Le statut du BT passe alors à <em>En cours</em> et l'heure de début est officiellement enregistrée.</li>
        <li><strong>Terminer une intervention</strong> : une fois les réparations achevées et les équipements remis en fonction, cliquez sur <strong>Terminer</strong>. Le statut passe à <em>Terminé</em> et l'heure de fin est sauvegardée, ce qui permet notamment de calculer le temps passé sur l'intervention.</li>
      </ul>

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
    </div>
  </v-container>
</template>

<script setup>
</script>

<style scoped>
.doc-page {
  padding: 0;
}
ul li {
  margin-bottom: 8px;
}
</style>
