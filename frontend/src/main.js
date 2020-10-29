import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;
Vue.filter('printDate', function (date) {
  if (!date) return date
  const date_obj = new Date(date)
  return date_obj.toLocaleDateString("en-US") + " " + date_obj.toLocaleTimeString("en-US")
})

Vue.filter('printNumber', function (number) {
  return parseFloat(number).toFixed(2);
})


export default new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
