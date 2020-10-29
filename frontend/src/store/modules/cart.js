import OrderService from "@/services/OrderService"
import router from "../../router";
import getErrMsg from "../../helpers"

export default {
  namespaced: true,
  state: {
    meals: [],
    error: "",
  },
  mutations: {
    add(state, meal) {
      state.meals.push(meal);
    },
    remove(state, idx) {
      state.meals.splice(idx, 1);
    },
    clear(state) {
      state.meals = [];
    },
    set(state, meals) {
      state.meals = meals;
    },
    error(state, msg) {
      state.error = msg;
    },
  },
  actions: {
    set({ commit, state }, meals) {
      commit("set", meals);
      localStorage.setItem("cart", JSON.stringify(state.meals));
    },
    add({ commit, state }, meal) {
      commit("add", meal);
      localStorage.setItem("cart", JSON.stringify(state.meals));
    },
    remove({ commit, state }, idx) {
      commit("remove", idx);
      localStorage.setItem("cart", JSON.stringify(state.meals));
    },
    clear({ commit, state }) {
      commit("clear");
      localStorage.setItem("cart", JSON.stringify(state.meals));
    },
    confirm({state, dispatch}) {
      const data = {
        restaurant_id: state.meals[0].restaurant.id,
        meal_ids: state.meals.map(m => m.id)
      }
      OrderService.create(data).then(() => {
        dispatch("clear");
        router.push("/orders");
      })
      .catch((error) =>  dispatch('msg/set', {msg: getErrMsg(error), type: 'error'}, {root: true}));
    },
    initialize({ commit }) {
      var meals = localStorage.getItem("cart");
      if (!meals) {
        return;
      }
      commit("set", JSON.parse(meals));
    },
  },
  getters: {
    meals(state) {
      return state.meals;
    },
    total(state) {
      return state.meals.reduce((sum, meal) => sum + meal.price, 0.0);
    },
    error(state) {
      return state.error;
    },
  },
};
