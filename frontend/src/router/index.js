import Vue from "vue";
import Router from "vue-router";
import Homepage from "./../components/Homepage.vue";
import Login from "./../components/auth/Login.vue";
import Register from "./../components/auth/Register.vue";
import RestaurantMine from "./../components/restaurant/Mine.vue";
import RestaurantAdd from "./../components/restaurant/Add.vue";
import MealAdd from "./../components/meal/Add.vue";
import MealMine from "./../components/meal/Mine.vue";
import OrderMine from "./../components/order/Mine.vue";

import store from "../store";

Vue.use(Router);

function requireAuth(to, from, next) {
  var user = store.getters["auth/user"];
  if (user) {
    next();
  } else {
    next("/login");
  }
}

function requireAuthOwner(to, from, next) {
  var user = store.getters["auth/user"];
  if (user && user.is_owner) {
    next();
  } else {
    next("/");
  }
}

export default new Router({
  routes: [
    { path: "/", component: Homepage, beforeEnter: requireAuth },
    { path: "/login", component: Login },
    { path: "/register", component: Register },
    {
      path: "/restaurant/add",
      name: "restaurant-add",
      component: RestaurantAdd,
      beforeEnter: requireAuthOwner,
    },
    {
      path: "/restaurants",
      name: "restaurants",
      component: RestaurantMine,
      beforeEnter: requireAuthOwner,
    },

    {
      path: "/meal/add",
      name: "meal-add",
      component: MealAdd,
      beforeEnter: requireAuthOwner,
    },
    {
      path: "/meals",
      name: "meals",
      component: MealMine,
      beforeEnter: requireAuth,
    },
    {
      path: "/orders",
      name: "orders",
      component: OrderMine,
      beforeEnter: requireAuth,
    },
  ],
});
