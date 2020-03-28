import Vue from "vue";
import Vuex from "vuex";
import { SERVER_CONFIGURATION, HTTP } from "./configuration";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {
    alert(state, data) {
      this.$alert(data);
    }
  },
  actions: {
    login(state, data) {
      return HTTP.post(SERVER_CONFIGURATION.endpoints.login(), data);
    },
    verifySession() {
      return HTTP.get(SERVER_CONFIGURATION.endpoints.verifySession());
    }
  },
  getters: {}
});
