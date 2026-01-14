import CreateModelEquipment from "../views/DataManagement/EquipmentsModels/CreateModelEquipment.vue";
import CreateLocation from "../views/DataManagement/Locations/CreateLocation.vue";
import SupplierDetail from "../views/DataManagement/Suppliers/SupplierDetail.vue";
import Stocks from "../views/Stocks/Stocks.vue";

export const BREADCRUMBS = {
    /***************************************
     * Équipements
     **************************************/
    EquipmentList: (route) => [
        {
            label: "Équipements",
            to: { name: "EquipmentList" },
        },
    ],

    CreateEquipment: (route) => [
        {
            label: "Équipements",
            to: { name: "EquipmentList" },
        },
        {
            label: "Créer un équipement",
        },
    ],

    EquipmentDetail: (route) => {
        if (route.query.from === "failure") {
            return [
                { label: "Demandes d'intervention", to: { name: "FailureList" } },
                {
                    label: `Demande d'intervention #${route.query.failureID}`,
                    to: {
                        name: "FailureDetail",
                        params: { id: route.query.failureID },
                    },
                },
                { label: `Équipement #${route.params.id}` },
            ];
        }

        return [{
            label: "Équipements",
            to: { name: "EquipmentList" },
        },
        {
            label: `Équipement #${route.params.id}`,
        }];
    },

    EditEquipment: (route) => [
        {
            label: "Equipements",
            to: { name: "EquipmentList" },
        },
        {
            label: `Equipement #${route.query.equipmentId}`,
            to: {
                name: "EquipmentDetail",
                params: { id: route.query.equipmentId },
            },
        },
        {
            label: "Modifier",
        },
    ],

    CounterDetail: (route) => [
        {
            label: "Equipements",
            to: { name: "EquipmentList" },
        },
        {
            label: `Equipement #${route.query.equipmentId}`,
            to: {
                name: "EquipmentDetail",
                params: { id: route.query.equipmentId },
            },
        },
        {
            label: `Compteur #${route.params.id}`,
        },
    ],

    /***************************************
     * Bons de travail
     **************************************/
    InterventionList: (route) => [
        {
            label: "Bons de travail",
            to: { name: "InterventionList" },
        },
    ],

    InterventionDetail: (route) => {
        if (route.query.from === "equipment") {
            return [
                { label: "Équipements", to: { name: "EquipmentList" } },
                {
                    label: `Équipement #${route.query.equipmentId}`,
                    to: {
                        name: "EquipmentDetail",
                        params: { id: route.query.equipmentId },
                    },
                },
                { label: `Intervention #${route.params.id}` },
            ];
        }

        // fallback : liste interventions
        return [
            { label: "Interventions", to: { name: "InterventionList" } },
            { label: `Intervention #${route.params.id}` },
        ];
    },

    /***************************************
     * Demandes d'intervention
     **************************************/
    FailureList: (route) => [
        {
            label: "Demandes d'intervention",
            to: { name: "FailureList" },
        },
    ],

    FailureDetail: (route) => [
        {
            label: "Demandes d'intervention",
            to: { name: "FailureList" },
        },
        {
            label: `Demande d'intervention #${route.params.id}`,
        },
    ],

    /***************************************
     * Magasin
     **************************************/
    Stocks: (route) => [
        {
            label: "Magasin",
            to: { name: "Stocks" },
        },
    ],

    /***************************************
     * Gestion des comptes
     **************************************/
    AccountManagement: (route) => [
        {
            label: "Gestion des comptes",
            to: { name: "AccountManagement" },
        },
    ],

    /***************************************
     * Gestion des données
     **************************************/
    DataManagement: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
    ],

    /***************************************
     * Dashboard
     **************************************/
    Dashboard: (route) => [
        {
            label: "Tableau de bord",
            to: { name: "Dashboard" },
        },
    ],

    /**************************************
     * Données secondaires
     **************************************/
    DataManagement: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
    ],

    // Lieux
    LocationList: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Lieux",
            to: { name: "LocationList" },
        },
    ],

    CreateLocation: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Lieux",
            to: { name: "LocationList" },
        },
        {
            label: "Créer un lieu",
        },
    ],

    // Fournisseurs
    SupplierList: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fournisseurs",
            to: { name: "SupplierList" },
        },
    ],

    CreateSupplier: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fournisseurs",
            to: { name: "SupplierList" },
        },
        {
            label: "Créer un fournisseur",
        },
    ],

    EditSupplier: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fournisseurs",
            to: { name: "SupplierList" },
        },
        {
            label: `Fournisseur #${route.params.id}`,
            to: {
                name: "SupplierDetail",
                params: { id: route.params.id },
            },
        },
        {
            label: "Modifier le fournisseur",
        },
    ],

    SupplierDetail: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fournisseurs",
            to: { name: "SupplierList" },
        },
        {
            label: `Fournisseur #${route.params.id}`,
        },
    ],

    // Fabricants
    ManufacturerList: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fabricants",
            to: { name: "ManufacturerList" },
        },
    ],

    CreateManufacturer: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fabricants",
            to: { name: "ManufacturerList" },
        },
        {
            label: "Créer un fabricant",
        },
    ],

    ManufacturerDetail: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fabricants",
            to: { name: "ManufacturerList" },
        },
        {
            label: `Fabricant #${route.params.id}`,
        },
    ],

    EditManufacturer: (route) => [  
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Fabricants",
            to: { name: "ManufacturerList" },
        },
        {
            label: `Fabricant #${route.params.id}`,
            to: {
                name: "ManufacturerDetail",
                params: { id: route.params.id },
            },
        },
        {
            label: "Modifier le fabricant",
        },
    ],

    // Modèles d'équipements
    ModelEquipmentList: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Modèles d'équipements",
            to: { name: "ModelEquipmentList" },
        },
    ],
    ModelEquipmentDetail: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Modèles d'équipements",
            to: { name: "ModelEquipmentList" },
        },
        {
            label: `Modèle d'équipement #${route.params.id}`,
        },
    ],
    CreateModelEquipment: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Modèles d'équipements",
            to: { name: "ModelEquipmentList" },
        },
        {
            label: "Créer un modèle d'équipement",
        },
    ],
    EditModelEquipment: (route) => [
        {
            label: "Gestion des données",
            to: { name: "DataManagement" },
        },
        {
            label: "Modèles d'équipements",
            to: { name: "ModelEquipmentList" },
        },
        {
            label: `Modèle d'équipement #${route.params.id}`,
            to: {
                name: "ModelEquipmentDetail",
                params: { id: route.params.id },
            },
        },
        {
            label: "Modifier le modèle d'équipement",
        },
    ],
};
