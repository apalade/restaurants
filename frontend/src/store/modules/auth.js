import Vue from "vue";
import Vuex from "vuex";
import router from "@/router";
import AuthService from "@/services/AuthService";
import getErrMsg from "../../helpers";

Vue.use(Vuex);

export default {
  namespaced: true,
  state: {
    user: null,
  },
  mutations: {
    authUser(state, user) {
      state.user = user;
    },
    clearAuth(state) {
      state.user = null;
    },
  },
  actions: {
    login({ commit, dispatch }, data) {
      AuthService.login(data)
        .then((res) => {
          localStorage.setItem("user", JSON.stringify(res.data));
          commit("authUser", res.data);
          router.push("/");
        })
        .catch((error) => {
          const payload = {
            msg: getErrMsg(error),
            type: "error",
          };
          dispatch("msg/set", payload, { root: true });
        });
    },
    logout({ commit, dispatch }) {
      commit("clearAuth");
      localStorage.removeItem("user");
      dispatch("cart/clear", {}, { root: true });
      router.replace("/login");
    },
    autologin({ commit }) {
      var user = localStorage.getItem("user");
      if (!user) {
        return;
      }
      commit("authUser", JSON.parse(user));
      router.replace("/");
    },
  },
  getters: {
    user(state) {
      return state.user;
    },
    ifAuth(state) {
      return state.user !== null;
    },
    ifAuthOwner(state, getters) {
      return getters.ifAuth && state.user.is_owner === true;
    },
  },
};
