<template>
  <BaseForm
    :title="isEditMode ? 'Modifier l\'utilisateur' : 'Créer un utilisateur'"
    :loading="loading"
    :error-message="errorMessage"
    :success-message="successMessage"
    :submit-button-text="isEditMode ? 'Enregistrer les modifications' : 'Créer l\'utilisateur'"
    @submit="handleSubmit"
    @cancel="$emit('close')"
    @clear-error="errorMessage = ''"
    @clear-success="successMessage = ''"
    actions-container-class="d-flex justify-end gap-2 mt-2"
  >
    <template #default>
      <v-sheet class="pa-4" elevation="1" rounded>
        <h4 class="mb-3">Informations</h4>
        <v-row dense>
          <v-col cols="12" md="6">
            <FormField
              v-model="form.nomUtilisateur"
              label="Nom d'utilisateur"
              :validation="validationSchema.nomUtilisateur"
              placeholder="jdupont, marie.martin..."
            />
          </v-col>

          <v-col cols="12" md="6">
            <FormField
              v-model="form.email"
              label="Email"
              type="email"
              :validation="validationSchema.email"
              placeholder="utilisateur@exemple.com"
            />
          </v-col>

          <v-col cols="12" md="6">
            <FormField
              v-model="form.prenom"
              label="Prénom"
              :validation="validationSchema.prenom"
              placeholder="Marie, Jean..."
            />
          </v-col>

          <v-col cols="12" md="6">
            <FormField
              v-model="form.nomFamille"
              label="Nom de famille"
              :validation="validationSchema.nomFamille"
              placeholder="Dupont, Martin..."
            />
          </v-col>

          <v-col cols="12" md="6">
            <FormSelect
              v-model="form.role"
              label="Rôle"
              :items="roleOptions"
              item-title="label"
              item-value="value"
              :validation="validationSchema.role"
              placeholder="Sélectionner un rôle"
            />
          </v-col>

          <v-col cols="12" md="6" class="d-flex align-center">
            <FormCheckbox
              v-model="form.actif"
              label="Compte actif"
            />
          </v-col>
        </v-row>
      </v-sheet>

      <!-- Section mot de passe uniquement en mode édition -->
      <v-sheet v-if="isEditMode" class="pa-4 mt-4" elevation="1" rounded>
        <h4 class="mb-3">Mot de passe</h4>
        <v-row dense>
          <v-col cols="12" md="6">
            <FormField
              v-model="passwordForm.ancien"
              label="Ancien mot de passe"
              type="password"
              placeholder="••••••••"
              hint="Laisser vide si l'utilisateur n'a pas encore de mot de passe (première définition)."
              persistent-hint
            />
          </v-col>

          <v-col cols="12" md="6" />

          <v-col cols="12" md="6">
            <FormField
              v-model="passwordForm.nouveau"
              label="Nouveau mot de passe"
              type="password"
              placeholder="••••••••"
              :validation="passwordValidation.nouveau"
            />
          </v-col>

          <v-col cols="12" md="6">
            <FormField
              v-model="passwordForm.confirmation"
              label="Confirmation nouveau mot de passe"
              type="password"
              placeholder="••••••••"
              :validation="passwordValidation.confirmation"
            />
          </v-col>

          <v-col cols="12" class="d-flex justify-end">
            <v-btn
              color="primary"
              :loading="isChangingPassword"
              :disabled="loading || isChangingPassword"
              type="button"
              @click="handlePasswordUpdate"
            >
              Mettre à jour le mot de passe
            </v-btn>
          </v-col>
        </v-row>
      </v-sheet>
    </template>
  </BaseForm>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import BaseForm from '@/components/common/BaseForm.vue';
import FormField from '@/components/Forms/inputType/FormField.vue';
import FormSelect from '@/components/Forms/inputType/FormSelect.vue';
import FormCheckbox from '@/components/Forms/inputType/FormCheckbox.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  utilisateurId: {
    type: [String, Number],
    default: null,
  },
});

const emit = defineEmits(['created', 'updated', 'close']);

const api = useApi(API_BASE_URL);

const loading = ref(false);
const isChangingPassword = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const roles = ref([]);
const originalData = ref(null);

const form = ref({
  nomUtilisateur: '',
  prenom: '',
  nomFamille: '',
  email: '',
  actif: true,
  role: null,
});

const passwordForm = ref({
  ancien: '',
  nouveau: '',
  confirmation: '',
});

const isEditMode = computed(() => !!props.utilisateurId);

const roleOptions = computed(() =>
  (roles.value || []).map((r) => ({
    label: r.nomRole,
    value: r.id,
  }))
);

const validationSchema = {
  nomUtilisateur: ['required', { name: 'minLength', params: [2] }],
  email: [
    'required',
    {
      name: 'regex',
      params: [/^[^\s@]+@[^\s@]+\.[^\s@]+$/],
      message: 'Email invalide',
    },
  ],
  prenom: ['required', { name: 'minLength', params: [2] }],
  nomFamille: ['required', { name: 'minLength', params: [2] }],
  role: ['required'],
};

const passwordValidation = {
  nouveau: [
    {
      name: 'custom',
      validate: (value) => !value || value.length >= 8,
      message: '8 caractères minimum',
    },
  ],
  confirmation: [
    {
      name: 'custom',
      validate: (value) => !passwordForm.value.nouveau || value === passwordForm.value.nouveau,
      message: 'Les mots de passe ne correspondent pas',
    },
  ],
};

const loadRoles = async () => {
  try {
    const result = await api.get('roles/');
    roles.value = Array.isArray(result) ? result : [];
  } catch (e) {
    console.error('Error loading roles:', e);
    roles.value = [];
  }
};

const loadUtilisateur = async () => {
  if (!props.utilisateurId) return;

  loading.value = true;
  errorMessage.value = '';

  try {
    const data = await api.get(`utilisateurs/${props.utilisateurId}/`);
    form.value = {
      nomUtilisateur: data?.nomUtilisateur ?? '',
      prenom: data?.prenom ?? '',
      nomFamille: data?.nomFamille ?? '',
      email: data?.email ?? '',
      actif: !!data?.actif,
      role: data?.role?.id ?? null,
    };
    originalData.value = JSON.parse(JSON.stringify(form.value));
  } catch (e) {
    console.error('Error loading utilisateur:', e);
    errorMessage.value = "Erreur lors du chargement de l'utilisateur.";
  } finally {
    loading.value = false;
  }
};

const detectChanges = () => {
  if (!isEditMode.value || !originalData.value) return null;

  const changes = {};
  const fields = ['nomUtilisateur', 'prenom', 'nomFamille', 'email', 'actif', 'role'];

  fields.forEach((field) => {
    const oldValue = originalData.value[field];
    const newValue = form.value[field];

    if (oldValue !== newValue) {
      changes[field] = {
        ancienne: oldValue,
        nouvelle: newValue,
      };
    }
  });

  return Object.keys(changes).length > 0 ? changes : null;
};

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    if (isEditMode.value) {
      const changes = detectChanges();
      if (!changes) {
        errorMessage.value = 'Aucune modification détectée.';
        loading.value = false;
        return;
      }

      await api.put(`utilisateurs/${props.utilisateurId}/`, {
        nomUtilisateur: form.value.nomUtilisateur,
        prenom: form.value.prenom,
        nomFamille: form.value.nomFamille,
        email: form.value.email,
        actif: form.value.actif,
        role_id: form.value.role,
      });

      successMessage.value = 'Utilisateur modifié avec succès.';
      setTimeout(() => {
        emit('updated', props.utilisateurId);
      }, 800);
    } else {
      const created = await api.post('utilisateurs/', {
        nomUtilisateur: form.value.nomUtilisateur,
        prenom: form.value.prenom,
        nomFamille: form.value.nomFamille,
        email: form.value.email,
        actif: form.value.actif,
        role: form.value.role,
      });

      successMessage.value = 'Utilisateur créé avec succès.';
      setTimeout(() => {
        emit('created', created);
      }, 800);
    }
  } catch (e) {
    console.error('Error saving utilisateur:', e);
    errorMessage.value = isEditMode.value
      ? "Erreur lors de la modification de l'utilisateur."
      : "Erreur lors de la création de l'utilisateur.";
  } finally {
    loading.value = false;
  }
};

const handlePasswordUpdate = async () => {
  if (!props.utilisateurId) {
    errorMessage.value = "Impossible de modifier le mot de passe : id manquant.";
    return;
  }

  errorMessage.value = '';
  successMessage.value = '';

  const ancien = passwordForm.value.ancien;
  const nouveau = passwordForm.value.nouveau;
  const confirmation = passwordForm.value.confirmation;

  const anyPasswordFieldFilled = !!(ancien || nouveau || confirmation);
  if (!anyPasswordFieldFilled) {
    errorMessage.value = 'Veuillez renseigner au moins le nouveau mot de passe.';
    return;
  }

  if (!nouveau || nouveau.length < 8) {
    errorMessage.value = 'Le nouveau mot de passe doit contenir au moins 8 caractères.';
    return;
  }

  if (!confirmation) {
    errorMessage.value = 'La confirmation du nouveau mot de passe est requise.';
    return;
  }

  if (nouveau !== confirmation) {
    errorMessage.value = 'Les mots de passe ne correspondent pas.';
    return;
  }

  isChangingPassword.value = true;
  try {
    if (ancien && ancien.trim() !== '') {
      await api.post(`utilisateurs/${props.utilisateurId}/changer_mot_de_passe/`, {
        ancien_motDePasse: ancien,
        nouveau_motDePasse: nouveau,
        nouveau_motDePasse_confirmation: confirmation,
      });
      successMessage.value = 'Mot de passe mis à jour avec succès.';
    } else {
      if (!form.value.nomUtilisateur) {
        errorMessage.value = "Nom d'utilisateur manquant : impossible de définir un mot de passe.";
        return;
      }

      await api.post('utilisateurs/definir_mot_de_passe/', {
        nomUtilisateur: form.value.nomUtilisateur,
        nouveau_motDePasse: nouveau,
        nouveau_motDePasse_confirmation: confirmation,
      });
      successMessage.value = 'Mot de passe défini avec succès.';
    }

    passwordForm.value = { ancien: '', nouveau: '', confirmation: '' };
  } catch (e) {
    const detail = e?.response?.data?.detail;
    if (typeof detail === 'string' && detail.trim() !== '') {
      errorMessage.value = detail;
    } else {
      errorMessage.value = "Erreur lors de la mise à jour du mot de passe.";
    }
  } finally {
    isChangingPassword.value = false;
  }
};

watch(() => props.utilisateurId, (newId) => {
  if (newId) {
    loadUtilisateur();
  }
}, { immediate: true });

onMounted(() => {
  loadRoles();
});
</script>
