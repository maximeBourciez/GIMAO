import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; 
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import './assets/css/global.css';  
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
  },
});

const app = createApp(App);

// Add favicon dynamically
const link = document.createElement('link');
link.setAttribute('rel', 'icon');
link.setAttribute('type', 'image/png');
link.setAttribute('href', require('@/assets/favicon.png'));
document.head.appendChild(link);

// Utilisez le store Vuex
app.use(store); 

// Utilisez le routeur
app.use(router);

// Utilisez Vuetify
app.use(vuetify);

// Fournir Vuetify à l'application
app.provide('vuetify', vuetify);

// Montez l'application
app.mount('#app');