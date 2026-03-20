<template>
  <v-container class="doc-page">
    <h4>Consulter et suivre les bons de travail</h4>

    <div class="text-body-2 mb-4 mt-2">
      La rubrique <strong>Bons de travail</strong> regroupe toutes les interventions planifiées ou en cours de réalisation. Elle vous permet de suivre l'évolution des maintenances, qu'elles soient correctives (suite à une panne) ou préventives (planifiées par un compteur).
      <br /><br />

      <strong>Informations visibles sur un Bon de Travail :</strong>
      <ul class="ml-4 mt-2 mb-4">
        <li><strong>Informations générales :</strong> le nom de l'intervention, la priorité et l'équipement concerné.</li>
        <li><strong>Planification :</strong> la date de création, la date de prise en charge prévue et la date d'échéance attendue.</li>
        <li><strong>Description & Consignes :</strong> le détail des opérations à réaliser ou le diagnostic initial.</li>
        <li><strong>Intervenants :</strong> le(s) technicien(s) assigné(s) à la tâche.</li>
        <li><strong>Ressources & Documents :</strong> les pièces détachées ou consommables nécessaires à l'intervention, ainsi que les documents joints (notices, schémas, photos).</li>
      </ul>

      <strong>Les différents statuts d'un Bon de Travail :</strong>
      <ul class="ml-4 mt-2 mb-4 list-unstyled">
        <li>- <strong>En attente</strong> : l'intervention est planifiée et assignée, mais le technicien n'a pas encore débuté le travail.</li>
        <li>- <strong>En cours</strong> : le technicien a signifié le démarrage de l'intervention (date de début enregistrée).</li>
        <li>- <strong>En retard</strong> : la date d'échéance prévue initialement a été dépassée sans que l'intervention ne soit terminée.</li>
        <li>- <strong>Terminé</strong> : le technicien a fini son intervention et rempli son compte-rendu.</li>
        <li>- <strong>Clôturé</strong> : le responsable a vérifié les travaux, mis à jour les stocks si nécessaire et fermé définitivement le BT.</li>
      </ul>

      <em>Note :</em> Un BT préventif est généré de manière automatique lorsqu'un compteur d'équipement (heures, kilomètres, cycles) atteint un seuil défini. Ces BT préventifs vous sont confiés de la même façon que les BT correctifs habituels.
    </div>
  </v-container>
</template>

<script setup>
</script>

<style scoped>
.doc-page {
  padding: 0;
}
ul.list-unstyled li {
  list-style-type: none;
  margin-bottom: 8px;
}
ul li {
  margin-bottom: 8px;
}
</style>
