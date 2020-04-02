import Vue from "vue";
import Vuex from "vuex";
import { SERVER_CONFIGURATION, HTTP } from "./configuration";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: {}
  },
  mutations: {
    alert(state, data) {
      this.$alert(data);
    },
    setUser(state, user) {
      Vue.set(state, "user", user);
    }
  },
  actions: {
    changePassword(state, data) {
      return HTTP.post(SERVER_CONFIGURATION.endpoints.changePassword(), data);
    },
    signup(state, data) {
      return HTTP.post(SERVER_CONFIGURATION.endpoints.signup(), data);
    },
    login(state, data) {
      return HTTP.post(SERVER_CONFIGURATION.endpoints.login(), data);
    },
    logout() {
      return HTTP.get(SERVER_CONFIGURATION.endpoints.logout());
    },
    verifySession() {
      return HTTP.get(SERVER_CONFIGURATION.endpoints.verifySession());
    }
  },
  getters: {
    user(state) {
      return state.user;
    }
  }
});
