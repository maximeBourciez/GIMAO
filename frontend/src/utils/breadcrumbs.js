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

		if (route.query.from === "intervention") {
			return [
				{ label: "Bons de travail", to: { name: "InterventionList" } },
				{
					label: `Bon de travail #${route.query.interventionId}`,
					to: {
						name: "InterventionDetail",
						params: { id: route.query.interventionId },
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
            { label: "Bons de travail", to: { name: "InterventionList" } },
            { label: `Bon de travail #${route.params.id}` },
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
};
