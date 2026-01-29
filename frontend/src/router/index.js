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
      requiresPermissions: ['user:viewList']
    }
  },

  {
    path: '/UserDetail/:id',
    name: 'UserDetail',
    component: AfficherUser,
    props: true,
    meta: {
      title: 'Afficher un utilisateur',
      requiresPermissions: ['user:viewDetail'],
      checksIfSelf: true
    }
  },

  {
    path: '/EditUser/:id',
    name: 'EditUser',
    component: ModifierUser,
    props: true,
    meta: { title: 'Modifier un utilisateur', requiresPermissions: ['user:edit'], checksIfSelf: true }
  },

  {
    path: '/CreateUser',
    name: 'CreateUser',
    component: CreerUser,
    meta: { title: 'Créer un utilisateur', requiresPermissions: ['user:create'] }
  },


  // Stocks & Consommables --------------------------------------------------------

  {
    path: '/stocks',
    name: 'Stocks',
    component: Stocks,
    meta: { title: 'Stocks', requiresPermissions: ['stock:view'] }
  },

  {
    path: '/CreateConsumable',
    name: 'CreateConsumable',
    component: CreateConsumable,
    meta: { title: 'Créer un consommable', requiresPermissions: ['cons:create'] }
  },

  {
    path: '/EditConsumable/:id',
    name: 'EditConsumable',
    component: CreateConsumable,
    props: true,
    meta: { title: 'Modifier un consommable', requiresPermissions: ['cons:edit'] }
  },

  {
    path: '/ConsumableDetail/:id',
    name: 'ConsumableDetail',
    component: CreateConsumable,
    props: true,
    meta: { title: 'Détails du consommable', requiresPermissions: ['cons:viewDetail'] }
  },

  {
    path: '/DeleteConsumable/:id',
    name: 'DeleteConsumable',
    component: CreateConsumable,
    props: true,
    meta: { title: 'Supprimer un consommable', requiresPermissions: ['cons:delete'] }
  },

  // Magasins
  {
    path: '/MagasinList',
    name: 'MagasinList',
    component: Stocks,
    meta: { title: 'Magasins', requiresPermissions: ['mag:viewList'] }
  },

  {
    path: '/MagasinDetail/:id',
    name: 'MagasinDetail',
    component: Stocks,
    props: true,
    meta: { title: 'Détails du magasin', requiresPermissions: ['mag:viewDetail'] }
  },

  {
    path: '/CreateMagasin',
    name: 'CreateMagasin',
    component: Stocks,
    meta: { title: 'Créer un magasin', requiresPermissions: ['mag:create'] }
  },

  {
    path: '/EditMagasin/:id',
    name: 'EditMagasin',
    component: Stocks,
    props: true,
    meta: { title: 'Modifier un magasin', requiresPermissions: ['mag:edit'] }
  },

  {
    path: '/DeleteMagasin/:id',
    name: 'DeleteMagasin',
    component: Stocks,
    props: true,
    meta: { title: 'Supprimer un magasin', requiresPermissions: ['mag:delete'] }
  },


  // Fabricants ------------------------------------------------------------------

  {
    path: '/ManufacturerList',
    name: 'ManufacturerList',
    component: ManufacturerList,
    meta: { title: 'Fabricants', requiresPermissions: ['man:viewList'] }
  },

  {
    path: '/CreateManufacturer',
    name: 'CreateManufacturer',
    component: CreateManufacturer,
    meta: { title: 'Creer un Fabricant', requiresPermissions: ['man:create'] }
  },

  {
    path: '/ManufacturerDetail/:id',
    name: 'ManufacturerDetail',
    component: ManufacturerDetail,
    props: true,
    meta: { title: 'Détails d\'un fabricant', requiresPermissions: ['man:viewDetail'] }
  },
  {
    path: '/EditManufacturer/:id',
    name: 'EditManufacturer',
    component: EditManufacturer,
    props: true,
    meta: { title: 'Modifier un Fabricant', requiresPermissions: ['man:edit'] }
  },

  // Fournisseurs ------------------------------------------------------------------

  {
    path: '/SupplierList',
    name: 'SupplierList',
    component: SupplierList,
    meta: { title: 'Fournisseurs', requiresPermissions: ['sup:viewList'] }
  },

  {
    path: '/CreateSupplier',
    name: 'CreateSupplier',
    component: CreateSupplier,
    meta: { title: 'Creer un Fournisseur', requiresPermissions: ['sup:create'] }
  },

  {
    path: '/SupplierDetail/:id',
    name: 'SupplierDetail',
    component: SupplierDetail,
    props: true,
    meta: { title: 'Détails d\'un Fournisseur', requiresPermissions: ['sup:viewDetail'] }
  },
  {
    path: '/EditSupplier/:id',
    name: 'EditSupplier',
    component: EditSupplier,
    props: true,
    meta: { title: 'Modifier un Fournisseur', requiresPermissions: ['sup:edit'] }
  },



  // GestionDonnees ---------------------------------------------------------------

  {
    path: '/DataManagement',
    name: 'DataManagement',
    component: DataManagement,
    meta: { title: 'Gestion des données', requiresPermissions: ['loc:viewList'] }
  },

  // Bon de travail ---------------------------------------------------------------

  {
    path: '/InterventionList',
    name: 'InterventionList',
    component: InterventionList,
    meta: { title: 'Bon de travail', requiresPermissions: ['bt:viewList'] }
  },

  {
    path: '/intervention/:id',
    name: 'InterventionDetail',
    component: InterventionDetail,
    props: true,
    meta: { title: 'Détails du bon de travail', requiresPermissions: ['bt:viewDetail'] }
  },

  {
    path: '/CreateIntervention/',
    name: 'CreateIntervention',
    component: CreateIntervention,
    meta: { title: 'Créer un bon de travail', requiresPermissions: ['bt:create'] }
  },

  {
    path: '/EditIntervention/:id',
    name: 'EditIntervention',
    component: EditIntervention,
    props: true,
    meta: { title: 'Modifier un bon de travail', requiresPermissions: ['bt:editAll', 'bt:editAssigned'], permissionMode: 'OR' }
  },

  {
    path: '/intervention/:id/AddDocumentIntervention',
    name: 'AddDocumentIntervention',
    component: AddDocumentIntervention,
    props: true,
    meta: { title: 'Ajouter un document au bon de travail', requiresPermissions: ['bt:editAll', 'bt:editAssigned'], permissionMode: 'OR' }
  },

  // Equipements ---------------------------------------------------------------

  {
    path: '/EquipmentList',
    name: 'EquipmentList',
    component: EquipmentList,
    meta: { title: 'Équipements', requiresPermissions: ['eq:viewList'] }
  },

  {
    path: '/EquipmentDetail/:id',
    name: 'EquipmentDetail',
    component: EquipmentDetail,
    props: true,
    meta: { title: 'Descriptif de l\'équipement', requiresPermissions: ['eq:viewDetail'] }
  },

  {
    path: '/CreateEquipment',
    name: 'CreateEquipment',
    component: CreateEquipment,
    meta: { title: 'Ajouter Equipement', requiresPermissions: ['eq:create'] }
  },

  {
    path: '/EditEquipment/:id',
    name: 'EditEquipment',
    component: EditEquipment,
    meta: { title: 'Modifier Equipement', requiresPermissions: ['eq:edit'] }
  },

  {
    path: '/CounterDetail/:id',
    name: 'CounterDetail',
    component: CounterDetail,
    meta: { title: 'Détails du compteur', requiresPermissions: ['cp:viewDetail'] }
  },

  // Defaillance ---------------------------------------------------------------
  {
    path: '/FailureList',
    name: 'FailureList',
    component: FailureList,
    meta: { title: 'Demandes d\'interventions', requiresPermissions: ['di:viewList'] }
  },

  {
    path: '/CreateFailure/:equipementReference?',
    name: 'CreateFailure',
    component: CreateFailure,
    props: true,
    meta: { title: 'Demande d\'intervention', requiresPermissions: ['di:create'] }
  },

  {
    path: '/Failure/:id',
    name: 'FailureDetail',
    component: FailureDetail,
    props: true,
    meta: { title: 'Détails de la demande ', requiresPermissions: ['di:viewDetail'] }
  },

  {
    path: '/Failure/:id/edit',
    name: 'EditFailure',
    component: EditFailure,
    props: true,
    meta: { title: 'Modifier la demande d\'intervention', requiresPermissions: ['di:editCreated', 'di:editAll'], permissionMode: 'OR' }
  },

  {
    path: '/Failure/:id/addDocument',
    name: 'AddDocumentFailure',
    component: AddDocumentFailure,
    props: true,
    meta: { title: 'Ajouter un document à la demande d\'intervention', requiresPermissions: ['di:editCreated', 'di:editAll'], permissionMode: 'OR' }
  },

  // Lieux ---------------------------------------------------------------

  {
    path: '/LocationList',
    name: 'LocationList',
    component: LocationList,
    meta: { title: 'Lieux', requiresPermissions: ['loc:viewList'] }
  },

  {
    path: '/CreateLocation',
    name: 'CreateLocation',
    component: CreateLocation,
    meta: { title: 'Creer un lieu', requiresPermissions: ['loc:create'] }
  },

  {
    path: '/LocationDetail/:id',
    name: 'LocationDetail',
    component: LocationDetail,
    props: true,
    meta: { title: 'Détails d\'un lieu', requiresPermissions: ['loc:viewDetail'] }
  },


  // Modele Equipements ---------------------------------------------------------------

  {
    path: '/ModelEquipmentList',
    name: 'ModelEquipmentList',
    component: ModelEquipmentList,
    meta: { title: 'Modèle', requiresPermissions: ['eqmod:viewList'] }
  },

  {
    path: '/CreateModelEquipment',
    name: 'CreateModelEquipment',
    component: CreateModelEquipment,
    meta: { title: 'Creer un modele equipement', requiresPermissions: ['eqmod:create'] }
  },

  {
    path: '/ModelEquipmentDetail/:id',
    name: 'ModelEquipmentDetail',
    component: ModelEquipmentDetail,
    meta: { title: 'Detail du modele equipement', requiresPermissions: ['eqmod:viewDetail'] }
  },
  {
    path: '/EditModelEquipment/:id',
    name: 'EditModelEquipment',
    component: EditModelEquipment,
    meta: { title: 'Modifier modele equipement', requiresPermissions: ['eqmod:edit'] }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Protection des routes
router.beforeEach((to, from, next) => {
  const userRaw = localStorage.getItem('user')
  const isAuthenticated = !!userRaw

  if (to.meta.public) {
    next()
    return
  }

  if (!isAuthenticated) {
    next('/login')
    return
  }

  const user = JSON.parse(userRaw)
  const userPermissions = user?.permissions_names || []

  const requiredPermissions = to.meta.requiresPermissions
  const permissionMode = to.meta.permissionMode || 'OR'

  // -----------------------------
  // Permissions
  // -----------------------------
  if (requiredPermissions && requiredPermissions.length > 0) {

    const hasPermission =
      permissionMode === 'AND'
        ? requiredPermissions.every(p => userPermissions.includes(p))
        : requiredPermissions.some(p => userPermissions.includes(p))

    if (!hasPermission) {

      // Cas spécial : self
      if (to.meta.checksIfSelf) {
        const userId = user.id
        const routeId = parseInt(to.params.id)

        if (userId === routeId) {
          next()
          return
        }
      }

      alert("Vous n'avez pas la permission d'accéder à cette page.")
      next(from.fullPath || '/')
      return
    }
  }

  next()
})



export default router