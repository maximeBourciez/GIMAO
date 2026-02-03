<template>
    <v-breadcrumbs class="breadcrumb" divider="›">
        <v-breadcrumbs-item v-for="(crumb, index) in breadcrumbs" :key="index"
            @click="crumb.route && $router.push(crumb.route)">
            {{ makeBreadcrumbLabel(crumb, index) }}
        </v-breadcrumbs-item>
    </v-breadcrumbs>
</template>


<script setup>
import { BREADCRUMBS, HEADERS } from '@/utils/breadcrumbs';
import { onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const breadcrumbs = ref([]);
const isInitialized = ref(false);

watch(route, () => {
    if (!route.name) return;

    if (!isInitialized.value) {
        if (localStorage.getItem('breadcrumb')) {
            const inBreadcrumbs = JSON.parse(localStorage.getItem('breadcrumb'));
            const matchIndex = inBreadcrumbs.findIndex(crumb => crumb.route === route.path);
            
            if (matchIndex !== -1) {
                // Found in history: restore up to parents
                breadcrumbs.value = inBreadcrumbs.slice(0, matchIndex);
            } else {
                // Not found in history: redirect to dashboard
                // Only redirect if we are not already at the dashboard to avoid loops
                if (route.name !== 'Dashboard') {
                    router.push({ name: 'Dashboard' });
                    return; // Stop execution, let the redirect trigger the next update
                }
            }
        }
        isInitialized.value = true;
    }

    // Standard breadcrumb update logic
    if (breadcrumbs.value.find(crumb => crumb.name === route.name)) {
        breadcrumbs.value = breadcrumbs.value.slice(0, breadcrumbs.value.findIndex(crumb => crumb.name === route.name));
    };
    if (HEADERS.includes(route.name)) {
        breadcrumbs.value.length = 0;
    }

    const lastMatch = route.matched[route.matched.length - 1];
    const showId = lastMatch?.path.endsWith('/:id');

    breadcrumbs.value.push({
        name:route.name,
        route: route.path,
        id: showId ? (route.params.id ?? null) : null,
    })
    console.log("saving breadcrumb", route.path)

    localStorage.setItem('breadcrumb', JSON.stringify(breadcrumbs.value));
}, { immediate: true })

function makeBreadcrumbLabel(crumb, index) {
    return `${BREADCRUMBS[crumb.name]} ${crumb.id ? `#${crumb.id}` : ''} ${index === breadcrumbs.length - 1 ? '' : '>' }`
}
</script>


<style scoped>
.breadcrumb {
    padding: 0 0 8px 0;
    font-size: 0.85rem;
    color: #6b7280;
    margin: 10px 0px 10px 15px;
    /* gris doux */
}

.breadcrumb .v-breadcrumbs-item {
    cursor: pointer;
    transition: color 0.2s ease;
}

.breadcrumb .v-breadcrumbs-item:not(.v-breadcrumbs-item--disabled):hover {
    color: #1976d2;
    /* primary Vuetify */
    text-decoration: underline;
}

.breadcrumb .v-breadcrumbs-item--disabled {
    color: #111827;
    /* plus foncé pour la page courante */
    font-weight: 600;
    cursor: default;
}
</style>