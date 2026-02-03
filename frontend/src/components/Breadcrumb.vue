<template>
    <v-breadcrumbs class="breadcrumb" divider="›">
        <v-breadcrumbs-item v-for="(crumb, index) in breadcrumbs" :key="index"
            @click="crumb.route && $router.push(crumb.route)">
            {{ makeBreadcrumb(crumb, index) }}
        </v-breadcrumbs-item>
    </v-breadcrumbs>
</template>


<script setup>
import { BREADCRUMBS, HEADERS } from '@/utils/breadcrumbs';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const breadcrumbs = ref([]);

watch(route, () => {
    if (breadcrumbs.value.find(crumb => crumb.name === route.name)) {
        breadcrumbs.value = breadcrumbs.value.slice(0, breadcrumbs.value.findIndex(crumb => crumb.name === route.name));
    };
    if (HEADERS.includes(route.name)) {
        breadcrumbs.value.length = 0;
    }
    console.log(route);
    const lastMatch = route.matched[route.matched.length - 1];
    const showId = lastMatch?.path.endsWith('/:id');

    breadcrumbs.value.push({
        name:route.name,
        route: route.path,
        id: showId ? (route.params.id ?? null) : null,
    })
})

function makeBreadcrumb(crumb, index) {
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