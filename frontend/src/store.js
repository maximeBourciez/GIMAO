import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    isAuthenticated: false
  },
  
  mutations: {
    setUser(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    
    logout(state) {
      state.user = null
      state.isAuthenticated = false
      localStorage.removeItem('user')
    }
  },
  
  actions: {
    initAuth({ commit }) {
      const user = localStorage.getItem('user')
      if (user) {
        try {
          commit('setUser', JSON.parse(user))
        } catch (e) {
          console.error('Erreur lors du chargement de l\'utilisateur:', e)
          localStorage.removeItem('user')
        }
      }
    },
    
    logout({ commit }) {
      commit('logout')
    }
  },
  
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    userRole: state => state.user?.role?.nomRole || null,
    userPermissions: state => state.user?.permissions || []
  },
  
  modules: {
    
  }
})