import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);

export default {
  namespaced: true,
  state: {
    msg: null,
    type: ''
  },
  mutations: {
    set(state, payload) {
      state.msg = payload.msg
      state.type = payload.type
    },
    clear(state) {
      state.msg = null;
    },
    
  },
  actions: {
    set({ commit }, payload) {
      commit("set", payload)
      setTimeout(() => {
        commit("clear");
      }, 2000);
     
    },
    clear({ commit }) {
      commit("clear");
    },
  },
  getters: {
    msg(state) {
      return state.msg;
    },
    type(state) {
      return state.type
    },
    exists(state) {
      return state.msg != null
    }
  },
};
