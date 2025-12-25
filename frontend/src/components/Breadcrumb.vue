<template>
    <v-breadcrumbs class="breadcrumb" divider="›">
        <v-breadcrumbs-item v-for="(crumb, index) in breadcrumbs" :key="index"
            :disabled="index === breadcrumbs.length - 1" @click="crumb.to && $router.push(crumb.to)">
            {{ crumb.label }} {{ index === breadcrumbs.length - 1 ? '' : '>' }}
        </v-breadcrumbs-item>
    </v-breadcrumbs>
</template>


<script>
import { BREADCRUMBS } from '@/utils/breadcrumbs';

export default {
    name: "Breadcrumb",
    computed: {
        breadcrumbs() {
            const routeName = this.$route.name;

            if (!routeName || !BREADCRUMBS[routeName]) {
                return [];
            }

            return BREADCRUMBS[routeName](this.$route);
        }
    }
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