import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';  

export const BASE_URL = 'http://localhost:8000';

export default {



  //Fournisseurs -----------------------

  getFournisseurs() {
    return axios.get(`${API_URL}fournisseurs/`);
  },

  getFournisseur(id) {
    return axios.get(`${API_URL}fournisseurs/${id}`);
  },

  postFournisseur(data) {
    return axios.post(`${API_URL}fournisseurs/`, data);
  },

  // Fabricants -----------------------

  getFabricants() {
    return axios.get(`${API_URL}fabricants/`);
  },

  getFabricant(id) {
    return axios.get(`${API_URL}fabricants/${id}`);
  },

  postFabricant(data) {
    return axios.post(`${API_URL}fabricants/`, data);
  },


  // ModeleEquipements -----------------------

  getModeleEquipements() {
    return axios.get(`${API_URL}modele-equipements/`);
  },

  getModeleEquipement(reference) {
    return axios.get(`${API_URL}modele-equipements/${reference}`);
  },

  postModeleEquipement(data) {
    return axios.post(`${API_URL}modele-equipements/`, data);
  },

  // Consommables -----------------------
  
  getConsommables() {
    return axios.get(`${API_URL}consommables/`);
  },

  getConsommable(reference) {
    return axios.get(`${API_URL}consommables/${reference}`);
  },

  postConsommable(data) {
    return axios.post(`${API_URL}consommables/`, data);
  },

  //Lieux -----------------------
  
  getLieuxHierarchy() {
    return axios.get(`${API_URL}lieux-hierarchy/`);
  },

  getLieux() {
    return axios.get(`${API_URL}lieux/`);
  },

  getLieu(reference) {
    return axios.get(`${API_URL}lieux/${reference}`);
  },

  postLieu(data) {
    return axios.post(`${API_URL}lieux/`, data);
  },

  // Equipements -----------------------

  getEquipements() {
    return axios.get(`${API_URL}equipements/`);
  },
  getEquipement(reference) {
    return axios.get(`${API_URL}equipements/${reference}`);
  },

  getEquipementsVue(){
    return axios.get(`${API_URL}equipements-detail/`);
  },

  postEquipement(data){
    return axios.post(`${API_URL}equipements/`, data);
  },

  getEquipementAffichage(reference) {
    return axios.get(`${API_URL}equipement/${reference}/affichage/`);
  },

  getEquipementAvecStatut(reference){
    return axios.get(`${API_URL}equipement/${reference}/avec-statut/`);
  },

  postConstituer(data){
    return axios.post(`${API_URL}constituer/`, data);
  },

  // Model Equipement-----------------------


  getModeleEquipements() {
    return axios.get(`${API_URL}modele-equipements/`);
  },

  // Intervention -----------------------

  
  getInterventions(){
    return axios.get(`${API_URL}interventions/`);
  },

  getInterventionAffichage(id) {
    return axios.get(`${API_URL}intervention/${id}/affichage/`);
  },

  postIntervention(data) {
    return axios.post(`${API_URL}interventions/`, data);
  },
  
  postInterventionDocument(data) {
    return axios.post(`${API_URL}document-interventions/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Utilisateur-----------------------

  getUtilisateur(){
    return axios.get(`${API_URL}utilisateurs/`);
  },


  // Statut -----------------------

  postInformationStatut(data) {
    return axios.post(`${API_URL}information-statuts/`, data);
  },
  
  // Defaillance -----------------------


  getDefaillances() {
    return axios.get(`${API_URL}defaillances/`);
  },

  getDefaillance(id) {
    return axios.get(`${API_URL}defaillances/${id}/`);
  },

  getDefaillanceAffichage(id) {
    return axios.get(`${API_URL}defaillance/${id}/affichage/`);
  },

  postDefaillance(data) {
    return axios.post(`${API_URL}defaillances/`, data);
  },

  patchDefaillance(defaillanceId, defaillanceData) {
    return axios.patch(`${API_URL}defaillances/${defaillanceId}/`, defaillanceData);
  },


  postDefaillanceDocument(data) {
    return axios.post(`${API_URL}document-defaillances/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  cloturerIntervention(id) {
    return axios.patch(`${API_URL}interventions/${id}/`, { dateCloture: new Date().toISOString() });
  },

};