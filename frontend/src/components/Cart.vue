<template>
  <div v-show="display" class="container cart">
    <div v-if="meals[0]">
      <h5 class="mb-0">Order</h5>
      <small
        >from <strong>{{ meals[0].restaurant.name }}</strong></small
      >
    </div>
    <div v-for="(el, idx) in meals" v-bind:key="idx" class="row mt-3">
      <div class="small ml-5 text-left">
        <strong>{{ el.name }}</strong><span class="text-muted"> @ </span>
        <strong>${{ el.price | printNumber }}</strong>
      
      <img
        height="16px"
        @click="remove(idx)"
        class="ml-2"
        src="https://icons.iconarchive.com/icons/paomedia/small-n-flat/16/sign-delete-icon.png"
      />
      </div>
    </div>
    <div class="mt-3">Total: <strong>${{ total | printNumber }}</strong></div>

    <a class="btn btn-primary m-2" @click="confirm">Confirm</a>
    <a class="btn btn-warning m-2" @click="clear">Clear</a>
  </div>
</template>

<script>
export default {
  name: "Cart",
  data() {
    return {};
  },
  computed: {
    auth() {
      return this.$store.getters["auth/ifAuth"];
    },
    authOwner() {
      return this.$store.getters["auth/ifAuthOwner"];
    },
    display() {
      return this.auth && this.meals.length > 0;
    },
    meals() {
      return this.$store.getters["cart/meals"];
    },
    total() {
      return this.$store.getters["cart/total"];
    },
  },
  methods: {
    clear() {
      this.$store.dispatch("cart/clear");
    },
    remove(idx) {
      this.$store.dispatch("cart/remove", idx);
    },
    confirm() {
      this.$store.dispatch("cart/confirm");
    },
  },
};
</script>

<style>
.cart {
  width: 20%;
  position: fixed;
  top: 0;
  right: 0;
  background: #ffffff;
  z-index: 1000;
}
</style>
