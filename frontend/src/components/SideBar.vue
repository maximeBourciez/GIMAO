<template>
    <v-navigation-drawer app permanent :width="drawerWidth" class="sidebar" @mouseenter="isHovered = true"
        @mouseleave="isHovered = false">
        <!-- Logo -->
        <v-list-item @click="$router.push({ name: 'Dashboard' })" class="text-center py-4 logo-item">
            <v-img :src="logo" contain max-width="80" class="mx-auto mb-2" />

            <v-list-item-title v-if="displayTitles" class="font-weight-bold text-h6">
                {{ appTitle }}
            </v-list-item-title>
        </v-list-item>

        <v-divider class="mb-2" />

        <!-- Navigation -->
        <v-list dense nav>
            <v-list-item v-for="item in navigationItems" :key="item.name"
                :to="!item.disabled ? { name: item.name } : null" :class="[
                    'my-1',
                    { 'active-item': isActive(item.name) },
                    { 'disabled-item': item.disabled }
                ]" @click="item.disabled ? $event.preventDefault() : null">
                <template #prepend>
                    <v-icon class="ml-3">{{ item.icon }}</v-icon>
                </template>

                <v-list-item-title v-html="item.title" :class="[
                    { 'hoverable': isMini },
                    { 'normal': !isMini }
                ]" />
            </v-list-item>
        </v-list>

        <!-- User / Logout -->
        <template #append>
            <div class="menu-toggle-wrapper">
                <v-btn variant="tonal" color="primary" class="menu-toggle-btn" @click="toggleMini">
                    <v-icon>
                        {{ isMini ? 'mdi-menu-open' : 'mdi-menu' }}
                    </v-icon>

                    <span v-if="!isMini" class="ml-2">
                        Réduire le menu
                    </span>
                    <span v-if="isHovered && isMini" class="ml-2">
                        {{ isMini ? 'Agrandir le menu' : 'Réduire le menu' }}
                    </span>
                </v-btn>
            </div>
            <v-divider />

            <v-list dense>
                <v-list-item class="py-2">
                    <template #prepend>
                        <v-avatar size="36" :color="userPhotoUrl ? 'transparent' : 'primary'">
                            <v-img v-if="userPhotoUrl" :src="userPhotoUrl" cover />
                            <span v-else class="text-white">{{ userInitials }}</span>
                        </v-avatar>
                    </template>

                    <template v-if="displayTitles">
                        <v-list-item-title>{{ user.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ user.role }}</v-list-item-subtitle>
                    </template>
                </v-list-item>

                <v-list-item class="logout-item" @click="logout">
                    <template #prepend>
                        <v-icon class="ml-3">mdi-logout</v-icon>
                    </template>

                    <v-list-item-title v-if="displayTitles">
                        Déconnexion
                    </v-list-item-title>
                </v-list-item>
            </v-list>
        </template>
    </v-navigation-drawer>
</template>

<script>
import { MEDIA_BASE_URL } from '@/utils/constants';

export default {
    name: "Sidebar",

    data() {
        return {
            appTitle: "GIMAO",
            logo: require("@/assets/images/LogoGIMAO.png"),

            isMini: false,    // choix utilisateur
            isHovered: false, // hover temporaire

            navigationItems: [
                { name: "Dashboard", icon: "mdi-view-dashboard", title: "Tableau de bord" },
                { name: "EquipmentList", icon: "mdi-tools", title: "Équipements" },
                { name: "InterventionList", icon: "mdi-wrench", title: "Bons de travail" },
                { name: "FailureList", icon: "mdi-alert", title: "Demandes d'interventions" },
                { name: "UserList", icon: "mdi-account-cog", title: "Gestion des comptes"},
                { name: "Stocks", icon: "mdi-package-variant-closed", title: "Stocks"},
                { name: "DataManagement", icon: "mdi-database-cog", title: "Gestion des données" }
            ]
        };
    },

    computed: {
        displayTitles() {
            return !this.isMini || this.isHovered;
        },

        drawerWidth() {
            return this.displayTitles ? 280 : 80;
        },

        currentUserRaw() {
            const currentUser = this.$store.getters.currentUser;
            if (currentUser) return currentUser;

            const userFromStorage = localStorage.getItem('user');
            if (!userFromStorage) return null;
            try {
                return JSON.parse(userFromStorage);
            } catch (e) {
                console.error('Error parsing user from localStorage:', e);
                return null;
            }
        },

        user() {
            const raw = this.currentUserRaw;
            if (!raw) {
                return { name: 'Utilisateur', role: 'Non défini' };
            }

            const prenom = raw?.prenom ?? '';
            const nomFamille = raw?.nomFamille ?? '';
            const displayName = `${prenom} ${nomFamille}`.trim() || raw?.nomUtilisateur || 'Utilisateur';
            return {
                name: displayName,
                role: raw?.role?.nomRole || 'Utilisateur'
            };
        },

        userPhotoUrl() {
            const raw = this.currentUserRaw;
            const path = raw?.photoProfil;
            if (!path || typeof path !== 'string' || path.trim() === '') return '';
            return `${MEDIA_BASE_URL}${path}`;
        },

        userInitials() {
            return this.user.name
                .split(" ")
                .map(w => w[0])
                .join("")
                .slice(0, 2)
                .toUpperCase();
        }
    },

    methods: {
        isActive(routeName) {
            return this.$route.name === routeName;
        },

        toggleMini() {
            this.isMini = !this.isMini;
        },

        logout() {
            // Supprimer les données du store et du localStorage
            this.$store.dispatch('logout');
            
            // Rediriger vers login avec un reload complet pour nettoyer tout le state
            window.location.href = '/login';
        }
    }
};
</script>

<style scoped>
.sidebar {
    transition: width 0.25s ease;
}

.logo-item {
    cursor: pointer;
}

/* =========================
   ITEM ACTIF
========================= */
.active-item {
    background-color: #5d5fef;
}

.active-item .v-list-item-title,
.active-item .v-icon {
    color: white !important;
}

.active-item:hover {
    background-color: #5d5fef !important;
}

/* =========================
   ITEM NORMAL
========================= */
.v-list-item-title {
    color: #151d48 !important;
}

/* Hover item NON actif */
.v-list-item:not(.active-item):hover {
    background-color: #f5f5f5;
}

/* Forcer couleur texte au hover (mini ou normal) */
.v-list-item:not(.active-item):hover .v-list-item-title,
.v-list-item:not(.active-item):hover .v-icon {
    color: #151d48 !important;
}

/* =========================
   DISABLED
========================= */
.disabled-item {
    pointer-events: none;
    opacity: 0.5;
    cursor: not-allowed;
}

/* =========================
   LOGOUT
========================= */
.logout-item:hover {
    background-color: #f5f5f5;
}

/* =========================
   TOGGLE DRAWER BUTTON
========================= */
.menu-toggle-wrapper {
    display: flex;
    justify-content: center;
    padding: 8px;
}

.menu-toggle-btn {
    width: 100%;
    max-width: 240px;
    /* ne dépasse jamais */
    font-weight: 600;
}

/* En mode mini → bouton carré centré */
.sidebar[style*="width: 80px"] .menu-toggle-btn {
    width: 48px;
    min-width: 48px;
    padding: 0;
}
</style>
