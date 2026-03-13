import { createStore } from "vuex";

export default createStore({

    state: {
        user: null,
        isAuthenticated: false,
        authTimestamp: null,
    },

    mutations: {
        setUser(state, user) {
            state.user = user;
            state.isAuthenticated = !!user;
            state.authTimestamp = Math.floor(Date.now() / 1000);

            localStorage.setItem("user", JSON.stringify(user));
            localStorage.setItem("authTimestamp", state.authTimestamp);
        },

        restoreAuth(state, { user, timestamp }) {
            state.user = user;
            state.isAuthenticated = true;
            state.authTimestamp = timestamp;
        },

        logout(state) {
            state.user = null;
            state.isAuthenticated = false;
            state.authTimestamp = null;
            localStorage.removeItem("user");
            localStorage.removeItem("authTimestamp");
        },
    },

    actions: {
        initAuth({ commit }) {
            const user = localStorage.getItem("user");
            const timestamp = localStorage.getItem("authTimestamp");

            if (user && timestamp) {
                try {
                    commit("restoreAuth", {
                        user: JSON.parse(user),
                        timestamp: parseInt(timestamp),
                    });
                } catch (e) {
                    console.error(
                        "Erreur lors du chargement de l'utilisateur:",
                        e,
                    );
                    localStorage.removeItem("user");
                    localStorage.removeItem("authTimestamp");
                }
            }
        },

        logout({ commit }) {
            commit("logout");
        },
    },

    getters: {
        isAuthenticated: (state) => state.isAuthenticated,
        currentUser: (state) => state.user,
        userRole: (state) => state.user?.role?.nomRole || null,
        authenticationDate: (state) =>
            state.authTimestamp ? new Date(state.authTimestamp * 1000) : null,
        userPermissions: (state) => state.user?.permissions_names || [],
        hasPermission: (state, getters) => (perm) => {
            if (!state.isAuthenticated) return false;
            return getters.userPermissions.includes(perm);
        },
    },

    modules: {},
});

export function checkAuthValidity(store) {
  return Math.floor(Date.now() / 1000) - parseInt(localStorage.getItem('authTimestamp') || '0') < 24 * 60 * 60; // 7 jours en secondes : 24 * 60 * 60
}