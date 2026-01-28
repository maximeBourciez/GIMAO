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
import Stocks from '@/views/Stocks/Stocks.vue'
import CreateConsumable from '@/views/Stocks/CreateConsumable.vue'
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
    meta: {
      title: 'Gestion des Comptes',
      requiresPermission: 'user:viewList'
    }
  },

  {
    path: '/UserDetail/:id',
    name: 'UserDetail',
    component: AfficherUser,
    props: true,
    meta: {
      title: 'Afficher un utilisateur',
      requiresPermission: 'user:viewDetail'
    }
  },

  {
    path: '/EditUser/:id',
    name: 'EditUser',
    component: ModifierUser,
    props: true,
    meta: { title: 'Modifier un utilisateur', requiresPermission: 'user:edit' }
  },

  {
    path: '/CreateUser',
    name: 'CreateUser',
    component: CreerUser,
    meta: { title: 'Créer un utilisateur', requiresPermission: 'user:create' }
  },


  // Stocks & Consommables --------------------------------------------------------

  {
    path: '/stocks',
    name: 'Stocks',
    component: Stocks,
    meta: { title: 'Stocks', requiresPermission: 'stocks:viewList' }
  },

  {
    path: '/CreateConsumable',
    name: 'CreateConsumable',
    component: CreateConsumable,
    meta: { title: 'Créer un consommable', requiresPermission: 'cons:create' }
  },

  {
    path: '/EditConsumable/:id',
    name: 'EditConsumable',
    component: CreateConsumable,
    props: true,
    meta: { title: 'Modifier un consommable', requiresPermission: 'cons:edit' }
  },

  {
    path: '/ConsumableDetail/:id',
    name: 'ConsumableDetail',
    component: CreateConsumable,
    props: true,
    meta: { title: 'Détails du consommable', requiresPermission: 'cons:viewDetail' }
  },

  {
    path: '/DeleteConsumable/:id',
    name: 'DeleteConsumable',
    component: CreateConsumable,
    props: true,
    meta: { title: 'Supprimer un consommable', requiresPermission: 'cons:delete' }
  },

  // Magasins
  {
    path: '/MagasinList',
    name: 'MagasinList',
    component: Stocks,
    meta: { title: 'Magasins', requiresPermission: 'mag:viewList' }
  },

  {
    path: '/MagasinDetail/:id',
    name: 'MagasinDetail',
    component: Stocks,
    props: true,
    meta: { title: 'Détails du magasin', requiresPermission: 'mag:viewDetail' }
  },

  {
    path: '/CreateMagasin',
    name: 'CreateMagasin',
    component: Stocks,
    meta: { title: 'Créer un magasin', requiresPermission: 'mag:create' }
  },

  {
    path: '/EditMagasin/:id',
    name: 'EditMagasin',
    component: Stocks,
    props: true,
    meta: { title: 'Modifier un magasin', requiresPermission: 'mag:edit' }
  },

  {
    path: '/DeleteMagasin/:id',
    name: 'DeleteMagasin',
    component: Stocks,
    props: true,
    meta: { title: 'Supprimer un magasin', requiresPermission: 'mag:delete' }
  },


  // Fabricants ------------------------------------------------------------------

  {
    path: '/ManufacturerList',
    name: 'ManufacturerList',
    component: ManufacturerList,
    meta: { title: 'Fabricants', requiresPermission: 'man:viewList' }
  },

  {
    path: '/CreateManufacturer',
    name: 'CreateManufacturer',
    component: CreateManufacturer,
    meta: { title: 'Creer un Fabricant', requiresPermission: 'man:create' }
  },

  {
    path: '/ManufacturerDetail/:id',
    name: 'ManufacturerDetail',
    component: ManufacturerDetail,
    props: true,
    meta: { title: 'Détails d\'un fabricant', requiresPermission: 'man:viewDetail' }
  },
  {
    path: '/EditManufacturer/:id',
    name: 'EditManufacturer',
    component: EditManufacturer,
    props: true,
    meta: { title: 'Modifier un Fabricant', requiresPermission: 'man:edit' }
  },

  // Fournisseurs ------------------------------------------------------------------

  {
    path: '/SupplierList',
    name: 'SupplierList',
    component: SupplierList,
    meta: { title: 'Fournisseurs', requiresPermission: 'sup:viewList' }
  },

  {
    path: '/CreateSupplier',
    name: 'CreateSupplier',
    component: CreateSupplier,
    meta: { title: 'Creer un Fournisseur', requiresPermission: 'sup:create' }
  },

  {
    path: '/SupplierDetail/:id',
    name: 'SupplierDetail',
    component: SupplierDetail,
    props: true,
    meta: { title: 'Détails d\'un Fournisseur', requiresPermission: 'sup:viewDetail' }
  },
  {
    path: '/EditSupplier/:id',
    name: 'EditSupplier',
    component: EditSupplier,
    props: true,
    meta: { title: 'Modifier un Fournisseur', requiresPermission: 'sup:edit' }
  },



  // GestionDonnees ---------------------------------------------------------------

  {
    path: '/DataManagement',
    name: 'DataManagement',
    component: DataManagement,
    meta: { title: 'Gestion des données', requiresPermission: 'loc:viewList' }
  },

  // Bon de travail ---------------------------------------------------------------

  {
    path: '/InterventionList',
    name: 'InterventionList',
    component: InterventionList,
    meta: { title: 'Bon de travail', requiresPermission: 'bt:viewList' }
  },

  {
    path: '/intervention/:id',
    name: 'InterventionDetail',
    component: InterventionDetail,
    props: true,
    meta: { title: 'Détails du bon de travail', requiresPermission: 'bt:viewDetail' }
  },

  {
    path: '/CreateIntervention/',
    name: 'CreateIntervention',
    component: CreateIntervention,
    meta: { title: 'Créer un bon de travail', requiresPermission: 'bt:create' }
  },

  {
    path: '/EditIntervention/:id',
    name: 'EditIntervention',
    component: EditIntervention,
    props: true,
    meta: { title: 'Modifier un bon de travail', requiresPermission: 'bt:edit' }
  },

  {
    path: '/intervention/:id/AddDocumentIntervention',
    name: 'AddDocumentIntervention',
    component: AddDocumentIntervention,
    props: true,
    meta: { title: 'Ajouter un document au bon de travail', requiresPermission: 'bt:edit' }
  },



  // Equipements ---------------------------------------------------------------

  {
    path: '/EquipmentList',
    name: 'EquipmentList',
    component: EquipmentList,
    meta: { title: 'Équipements', requiresPermission: 'eq:viewList' }
  },

  {
    path: '/EquipmentDetail/:id',
    name: 'EquipmentDetail',
    component: EquipmentDetail,
    props: true,
    meta: { title: 'Descriptif de l\'équipement', requiresPermission: 'eq:viewDetail' }
  },

  {
    path: '/CreateEquipment',
    name: 'CreateEquipment',
    component: CreateEquipment,
    meta: { title: 'Ajouter Equipement', requiresPermission: 'eq:create' }
  },

  {
    path: '/EditEquipment/:id',
    name: 'EditEquipment',
    component: EditEquipment,
    meta: { title: 'Modifier Equipement', requiresPermission: 'eq:edit' }
  },

  {
    path: '/CounterDetail/:id',
    name: 'CounterDetail',
    component: CounterDetail,
    meta: { title: 'Détails du compteur', requiresPermission: 'cp:viewDetail' }
  },

  // Defaillance ---------------------------------------------------------------
  {
    path: '/FailureList',
    name: 'FailureList',
    component: FailureList,
    meta: { title: 'Demandes d\'interventions', requiresPermission: 'di:viewList' }
  },

  {
    path: '/CreateFailure/:equipementReference?',
    name: 'CreateFailure',
    component: CreateFailure,
    props: true,
    meta: { title: 'Demande d\'intervention', requiresPermission: 'di:create' }
  },

  {
    path: '/Failure/:id',
    name: 'FailureDetail',
    component: FailureDetail,
    props: true,
    meta: { title: 'Détails de la demande ', requiresPermission: 'di:viewDetail' }
  },

  {
    path: '/Failure/:id/edit',
    name: 'EditFailure',
    component: EditFailure,
    props: true,
    meta: { title: 'Modifier la demande d\'intervention', requiresPermission: 'di:edit' }
  },

  {
    path: '/Failure/:id/addDocument',
    name: 'AddDocumentFailure',
    component: AddDocumentFailure,
    props: true,
    meta: { title: 'Ajouter un document à la demande d\'intervention', requiresPermission: 'di:edit' }
  },

  // Lieux ---------------------------------------------------------------

  {
    path: '/LocationList',
    name: 'LocationList',
    component: LocationList,
    meta: { title: 'Lieux', requiresPermission: 'loc:viewList' }
  },

  {
    path: '/CreateLocation',
    name: 'CreateLocation',
    component: CreateLocation,
    meta: { title: 'Creer un lieu', requiresPermission: 'loc:create' }
  },

  {
    path: '/LocationDetail/:id',
    name: 'LocationDetail',
    component: LocationDetail,
    props: true,
    meta: { title: 'Détails d\'un lieu', requiresPermission: 'loc:viewDetail' }
  },


  // Modele Equipements ---------------------------------------------------------------

  {
    path: '/ModelEquipmentList',
    name: 'ModelEquipmentList',
    component: ModelEquipmentList,
    meta: { title: 'Modèle', requiresPermission: 'eqmod:viewList' } 
  },

  {
    path: '/CreateModelEquipment',
    name: 'CreateModelEquipment',
    component: CreateModelEquipment,
    meta: { title: 'Creer un modele equipement', requiresPermission: 'eqmod:create' }
  },

  {
    path: '/ModelEquipmentDetail/:id',
    name: 'ModelEquipmentDetail',
    component: ModelEquipmentDetail,
    meta: { title: 'Detail du modele equipement', requiresPermission: 'eqmod:viewDetail' }
  },
  {
    path: '/EditModelEquipment/:id',
    name: 'EditModelEquipment',
    component: EditModelEquipment,
    meta: { title: 'Modifier modele equipement', requiresPermission: 'eqmod:edit' }
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

  // Vérification des permissions si nécessaire
  const requiredPermission = to.meta.requiresPermission
  if (requiredPermission) {
    const user = JSON.parse(localStorage.getItem('user'))
    const userPermissions = user?.permissions_names || []

    if (!userPermissions.includes(requiredPermission)) {
      alert("Vous n'avez pas la permission d'accéder à cette page.")
      // Revenir à la page précédente ou au dashboard
      next(from.fullPath || '/')
      return
    }
  }

  // Si non authentifié, rediriger vers login
  if (!isAuthenticated) {
    next('/login')
    return
  }

  next()
})

export default router