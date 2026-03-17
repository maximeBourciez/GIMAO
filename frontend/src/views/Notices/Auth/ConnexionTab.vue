<template>
  <div>
    <div class="text-body-1 font-weight-bold mb-2">
      Connexion à l’application
    </div>

    <div class="text-body-2 mb-4">
      <strong>Accéder à l’application :</strong><br /><br />

      1. Ouvrez votre navigateur web<br />
      2. Saisissez l’adresse suivante : <strong>http://51.91.252.46</strong><br />
      3. Sur la page de connexion :<br />
      &nbsp;&nbsp;• Entrez votre nom d’utilisateur fourni par le responsable GMAO<br />
      &nbsp;&nbsp;• Cliquez sur <strong>Se connecter</strong>
    </div>

    <ZoomImage src="/images/login.png" alt="Page de connexion" />

    <div class="text-body-2 mt-4 mb-4">
      <strong>Première connexion :</strong><br /><br />
      Lors de votre première connexion, vous devrez définir un mot de passe afin de sécuriser votre compte.
    </div>

    <div class="text-body-2 mb-4">
      <strong>Connexion classique :</strong><br /><br />
      Si un mot de passe est déjà défini :
      <br />
      &nbsp;&nbsp;• Un champ mot de passe apparaît après avoir cliqué sur <strong>Se connecter</strong><br />
      &nbsp;&nbsp;• Saisissez votre mot de passe<br />
      &nbsp;&nbsp;• Cliquez à nouveau sur <strong>Se connecter</strong>
    </div>

    <div class="text-body-2">
      Une fois connecté, vous accédez à votre <strong>tableau de bord</strong>, adapté à votre rôle dans l’application.
    </div>
  </div>
</template>

<script setup>
import ZoomImage from "../common/ZoomImage.vue";
</script>