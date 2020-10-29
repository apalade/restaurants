<template>
  <div id="app">
    <h2></h2>
    <Menu />
    <div class="cart">
      <Cart />
    </div>
    <Message />

    <router-view />
  </div>
</template>

<script>
import Menu from "./components/Menu.vue";
import Cart from "./components/Cart.vue";
import Message from "./components/Message.vue";


export default {
  name: "App",
  components: {
    Cart,
    Menu,
    Message,
  },
  created() {
    this.$store.dispatch("auth/autologin");
    this.$store.dispatch("cart/initialize");
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

</style>
