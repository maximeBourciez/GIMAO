<template>
    <v-card>
        <v-card-title>
            Ajouter un équipement
        </v-card-title>

        <v-card-text>
            <v-row dense>
                <!-- Nom -->
                <v-col cols="12">
                    <v-text-field v-model="equipment.nom" label="Nom de l’équipement *" outlined dense
                        :error="submitted && !equipment.nom.trim()" />
                </v-col>

                <!-- Fabricant -->
                <v-col cols="12">
                    <v-select v-model="equipment.fabricant" :items="fabricants" item-title="nom" item-value="id"
                        label="Fabricant *" outlined dense clearable>
                        <template #append-item>
                            <v-divider />
                            <v-list-item class="text-primary" @click="showFabricantModal = true">
                                <v-list-item-title>
                                    ➕ Ajouter un fabricant
                                </v-list-item-title>
                            </v-list-item>
                        </template>
                    </v-select>
                </v-col>
            </v-row>
        </v-card-text>

        <v-card-actions>
            <v-spacer />
            <v-btn text @click="$emit('close')">Annuler</v-btn>
            <v-btn color="primary" @click="submit">
                Enregistrer
            </v-btn>
        </v-card-actions>

        <!-- Modale fabricant -->
        <v-dialog v-model="showFabricantModal" max-width="600">
            <FabricantForm @save="onFabricantCreated" @close="showFabricantModal = false" />
        </v-dialog>
    </v-card>
</template>


<script setup>
import { ref } from 'vue'
import FabricantForm from '@/components/FabricantForm.vue'

const props = defineProps({
    fabricants: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['save', 'close'])

const submitted = ref(false)
const showFabricantModal = ref(false)

const equipment = ref({
    nom: '',
    fabricant: null
})

const submit = () => {
    submitted.value = true

    if (!equipment.value.nom.trim()) return
    if (!equipment.value.fabricant) return

    emit('save', equipment.value)
}

</script>
