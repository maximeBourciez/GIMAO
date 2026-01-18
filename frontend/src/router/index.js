import { createRouter, createWebHistory } from 'vue-router'

// ---------------------------------------------------------------
// AUTH
import Login from '@/views/Auth/Login.vue'
import SetPassword from '@/views/Auth/SetPassword.vue'

// ---------------------------------------------------------------
import Dashboard from '@/views/Dashboard/Dashboard.vue'
import EquipmentList from '@/views/Equipments/EquipmentList.vue'
import InterventionList from '@/views/Interventions/InterventionList.vue'
import AccountManagement from '@/views/Users/UserList.vue'
import AfficherUser from '@/views/Users/UserDetail.vue'
import ModifierUser from '@/views/Users/EditUser.vue'
import CreerUser from '@/views/Users/CreateUser.vue'
import Orders from '@/views/Orders/Orders.vue'
import Stocks from '@/views/Stocks/Stocks.vue'
import FailureList from '@/views/Failures/FailureList.vue'


// ---------------------------------------------------------------
import InterventionDetail from '@/views/Interventions/InterventionDetail.vue'
import CreateIntervention from '@/views/Interventions/CreateIntervention.vue'
import EditIntervention from '@/views/Interventions/EditIntervention.vue'
import AddDocumentIntervention from '@/views/Interventions/AddDocumentIntervention.vue'

// ------------------------------------------------------------------
import EquipmentDetail from '@/views/Equipments/EquipmentDetail.vue'
import CreateEquipment from '@/views/Equipments/CreateEquipment.vue'
import EditEquipment from '@/views/Equipments/EditEquipment.vue'

// ------------------------------------------------------------------
import CreateFailure from '@/views/Failures/CreateFailure.vue'
import FailureDetail from '@/views/Failures/FailureDetail.vue'
import EditFailure from '@/views/Failures/EditFailure.vue'
import AddDocumentFailure from '@/views/Failures/AddDocumentFailure.vue'

// ------------------------------------------------------------------

import DataManagement from '@/views/DataManagement/DataManagement.vue'

import CreateLocation from '@/views/DataManagement/Locations/CreateLocation.vue'
import LocationList from '@/views/DataManagement/Locations/LocationList.vue'
import LocationDetail from '@/views/DataManagement/Locations/LocationDetail.vue'

import CreateSupplier from '@/views/DataManagement/Suppliers/CreateSupplier.vue'
import SupplierList from '@/views/DataManagement/Suppliers/SupplierList.vue'
import SupplierDetail from '@/views/DataManagement/Suppliers/SupplierDetail.vue'

import CreateManufacturer from '@/views/DataManagement/Manufacturers/CreateManufacturer.vue'
import ManufacturerList from '@/views/DataManagement/Manufacturers/ManufacturerList.vue'
import ManufacturerDetail from '@/views/DataManagement/Manufacturers/ManufacturerDetail.vue'
import EditManufacturer from '../views/DataManagement/Manufacturers/EditManufacturer.vue'

import ModelEquipmentList from '@/views/DataManagement/EquipmentsModels/ModelEquipmentList.vue'
import CreateModelEquipment from '@/views/DataManagement/EquipmentsModels/CreateModelEquipment.vue'
import ModelEquipmentDetail from '@/views/DataManagement/EquipmentsModels/ModelEquipmentDetail.vue'
import EditModelEquipment from '@/views/DataManagement/EquipmentsModels/EditModelEquipment.vue'

import CounterDetail from '@/views/Equipments/Counters/CounterDetail.vue'
import EditSupplier from '@/views/DataManagement/Suppliers/EditSupplier.vue'


const routes = [
  // Auth routes (publiques)
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true }
  },
  {
    path: '/set-password',
    name: 'SetPassword',
    component: SetPassword,
    meta: { public: true }
  },

  // Routes protégées
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Tableau de Bord' }
  },

  {
    path: '/UserList',
    name: 'UserList',
    component: AccountManagement,
    meta: { title: 'Gestion des Comptes' }
  },

  {
    path: '/UserDetail/:id',
    name: 'UserDetail',
    component: AfficherUser,
    props: true,
    meta: { title: 'Afficher un utilisateur' }
  },

  {
    path: '/EditUser/:id',
    name: 'EditUser',
    component: ModifierUser,
    props: true,
    meta: { title: 'Modifier un utilisateur' }
  },

  {
    path: '/CreateUser',
    name: 'CreateUser',
    component: CreerUser,
    meta: { title: 'Créer un utilisateur' }
  },

  {
    path: '/Orders',
    name: 'Orders',
    component: Orders,
    meta: { title: 'Commandes' }

  },

  {
    path: '/stocks',
    name: 'Stocks',
    component: Stocks,
    meta: { title: 'Stocks' }
  },



  // Consommables ------------------------------------------------------------------




  // Fabricants ------------------------------------------------------------------

  {
    path: '/ManufacturerList',
    name: 'ManufacturerList',
    component: ManufacturerList,
    meta: { title: 'Fabricants' }
  },

  {
    path: '/CreateManufacturer',
    name: 'CreateManufacturer',
    component: CreateManufacturer,
    meta: { title: 'Creer un Fabricant' }
  },

  {
    path: '/ManufacturerDetail/:id',
    name: 'ManufacturerDetail',
    component: ManufacturerDetail,
    props: true,
    meta: { title: 'Détails d\'un fabricant' }
  },
  {
    path: '/EditManufacturer/:id',
    name: 'EditManufacturer',
    component: EditManufacturer,
    props: true,
    meta: { title: 'Modifier un Fabricant' }
  },

  // Fournisseurs ------------------------------------------------------------------

  {
    path: '/SupplierList',
    name: 'SupplierList',
    component: SupplierList,
    meta: { title: 'Fournisseurs' }
  },

  {
    path: '/CreateSupplier',
    name: 'CreateSupplier',
    component: CreateSupplier,
    meta: { title: 'Creer un Fournisseur' }
  },

  {
    path: '/SupplierDetail/:id',
    name: 'SupplierDetail',
    component: SupplierDetail,
    props: true,
    meta: { title: 'Détails d\'un Fournisseur' }
  },
  {
    path: '/EditSupplier/:id',
    name: 'EditSupplier',
    component: EditSupplier,
    props: true,
    meta: { title: 'Modifier un Fournisseur' }
  },



  // GestionDonnees ---------------------------------------------------------------

  {
    path: '/DataManagement',
    name: 'DataManagement',
    component: DataManagement,
    meta: { title: 'Gestion des données' }
  },

  // Bon de travail ---------------------------------------------------------------

  {
    path: '/InterventionList',
    name: 'InterventionList',
    component: InterventionList,
    meta: { title: 'Bon de travail' }
  },

  {
    path: '/intervention/:id',
    name: 'InterventionDetail',
    component: InterventionDetail,
    props: true,
    meta: { title: 'Détails du bon de travail' }
  },

  {
    path: '/CreateIntervention/',
    name: 'CreateIntervention',
    component: CreateIntervention,
    meta: { title: 'Créer un bon de travail' }
  },

  {
    path: '/EditIntervention/:id',
    name: 'EditIntervention',
    component: EditIntervention,
    props: true,
    meta: { title: 'Modifier un bon de travail' }
  },

  {
    path: '/intervention/:id/AddDocumentIntervention',
    name: 'AddDocumentIntervention',
    component: AddDocumentIntervention,
    props: true,
    meta: { title: 'Ajouter un document au bon de travail' }
  },



  // Equipements ---------------------------------------------------------------

  {
    path: '/EquipmentList',
    name: 'EquipmentList',
    component: EquipmentList,
    meta: { title: 'Équipements' }
  },

  {
    path: '/EquipmentDetail/:id',
    name: 'EquipmentDetail',
    component: EquipmentDetail,
    props: true,
    meta: { title: 'Descriptif de l\'équipement' }
  },

  {
    path: '/CreateEquipment',
    name: 'CreateEquipment',
    component: CreateEquipment,
    meta: { title: 'Ajouter Equipement' }
  },

  {
    path: '/EditEquipment/:id',
    name: 'EditEquipment',
    component: EditEquipment,
    meta: { title: 'Modifier Equipement' }
  },

  {
    path: '/CounterDetail/:id',
    name: 'CounterDetail',
    component: CounterDetail,
    meta: { title: 'Détails du compteur' }
  },

  // Defaillance ---------------------------------------------------------------
  {
    path: '/FailureList',
    name: 'FailureList',
    component: FailureList,
    meta: { title: 'Demandes d\'interventions' }
  },

  {
    path: '/CreateFailure/:equipementReference?',
    name: 'CreateFailure',
    component: CreateFailure,
    props: true,
    meta: { title: 'Demande d\'intervention' }
  },

  {
    path: '/Failure/:id',
    name: 'FailureDetail',
    component: FailureDetail,
    props: true,
    meta: { title: 'Détails de la demande ' }
  },

  {
    path: '/Failure/:id/edit',
    name: 'EditFailure',
    component: EditFailure,
    props: true,
    meta: { title: 'Modifier la demande d\'intervention' }
  },

  {
    path: '/Failure/:id/addDocument',
    name: 'AddDocumentFailure',
    component: AddDocumentFailure,
    props: true,
    meta: { title: 'Ajouter un document à la demande d\'intervention' }
  },

  // Lieux ---------------------------------------------------------------

  {
    path: '/LocationList',
    name: 'LocationList',
    component: LocationList,
    meta: { title: 'Lieux' }
  },

  {
    path: '/CreateLocation',
    name: 'CreateLocation',
    component: CreateLocation,
    meta: { title: 'Creer un lieu' }
  },

  {
    path: '/LocationDetail/:id',
    name: 'LocationDetail',
    component: LocationDetail,
    props: true,
    meta: { title: 'Détails d\'un lieu' }
  },


  // Modele Equipements ---------------------------------------------------------------

  {
    path: '/ModelEquipmentList',
    name: 'ModelEquipmentList',
    component: ModelEquipmentList,
    meta: { title: 'Modèle' }
  },

  {
    path: '/CreateModelEquipment',
    name: 'CreateModelEquipment',
    component: CreateModelEquipment,
    meta: { title: 'Creer un modele equipement' }
  },

  {
    path: '/ModelEquipmentDetail/:id',
    name: 'ModelEquipmentDetail',
    component: ModelEquipmentDetail,
    meta: { title: 'Detail du modele equipement' }
  },
  {
    path: '/EditModelEquipment/:id',
    name: 'EditModelEquipment',
    component: EditModelEquipment,
    meta: { title: 'Modifier modele equipement' }
  }


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Protection des routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('user')

  // Si la route est publique, laisser passer
  if (to.meta.public) {
    next()
    return
  }

  // Si non authentifié, rediriger vers login
  if (!isAuthenticated) {
    next('/login')
    return
  }

  next()
})

export default router