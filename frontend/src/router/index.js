import { createRouter, createWebHistory } from 'vue-router'

// ---------------------------------------------------------------
import Dashboard from '@/views/Dashboard/Dashboard.vue'
import EquipmentList from '@/views/Equipments/EquipmentList.vue'
import InterventionList from '@/views/Interventions/InterventionList.vue'
import Technicians from '@/views/Technicians/Technicians.vue'
import AccountManagement from '@/views/AccountManagement/AccountManagement.vue'
import Orders from '@/views/Orders/Orders.vue'
import Stocks from '@/views/Stocks/Stocks.vue'
import FailureList from '@/views/Failures/FailureList.vue'


// ---------------------------------------------------------------
import InterventionDetail from '@/views/Interventions/InterventionDetail.vue'
import CreateIntervention from '@/views/Interventions/CreateIntervention.vue'
import AddDocumentIntervention from '@/views/Interventions/AddDocumentIntervention.vue'

// ------------------------------------------------------------------
import EquipmentDetail from '@/views/Equipments/EquipmentDetail.vue'
import CreateEquipment from '@/views/Equipments/CreateEquipment.vue'
import EditEquipment from '@/views/Equipments/EditEquipment.vue'

// ------------------------------------------------------------------
import CreateFailure from '@/views/Failures/CreateFailure.vue'
import FailureDetail from '@/views/Failures/FailureDetail.vue'
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

import ConsumableList from '@/views/DataManagement/Consumables/ConsumableList.vue'
import CreateConsumable from '@/views/DataManagement/Consumables/CreateConsumable.vue'
import ConsumableDetail from '@/views/DataManagement/Consumables/ConsumableDetail.vue'

import ModelEquipmentList from '@/views/DataManagement/EquipmentsModels/ModelEquipmentList.vue'
import CreateModelEquipment from '@/views/DataManagement/EquipmentsModels/CreateModelEquipment.vue'
import ModelEquipmentDetail from '@/views/DataManagement/EquipmentsModels/ModelEquipmentDetail.vue'




const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Tableau de Bord' }
  },

  {
    path: '/Technicians',
    name: 'Technicians',
    component: Technicians,
    meta: { title: 'Techniciens' }
  },

  {
    path: '/AccountManagement',
    name: 'AccountManagement',
    component: AccountManagement,
    meta: { title: 'Gestion des Comptes' }
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

  {
    path: '/ConsumableList',
    name: 'ConsumableList',
    component: ConsumableList,
    meta: { title: 'Consommables' }
  },

  {
    path: '/CreateConsumable',
    name: 'CreateConsumable',
    component: CreateConsumable,
    meta: { title: 'Creer un Consommable' }
  },

  {
    path: '/ConsumableDetail/:id',
    name: 'ConsumableDetail',
    component: ConsumableDetail,
    props: true,
    meta: { title: 'Détails d\'un consommable' }
  },


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



  // GestionDonnees ---------------------------------------------------------------

  {
    path: '/DataManagement',
    name: 'DataManagement',
    component: DataManagement,
    meta: { title: 'Gestion des données' }
  },

  // Interventions ---------------------------------------------------------------

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
    meta: { title: 'Détails de l\'intervention' }
  },

  {
    path: '/defaillance/:id/CreateIntervention/',
    name: 'CreateIntervention',
    component: CreateIntervention,
    meta: { title: 'Créer un bon de travail' }
  },

  {
    path: '/intervention/:id/AddDocumentIntervention',
    name: 'AddDocumentIntervention',
    component: AddDocumentIntervention,
    props: true,
    meta: { title: 'Détails de l\'intervention' }
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


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router