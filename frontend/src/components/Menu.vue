<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#"></a>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarText"
      aria-controls="navbarText"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarText">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <router-link class="nav-link" to="/">
            Home
            <span class="sr-only">(current)</span>
          </router-link>
        </li>
        <li v-if="!auth" class="nav-item">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li v-if="!auth" class="nav-item">
          <router-link class="nav-link" to="/register">Register</router-link>
        </li>
        <li v-if="authOwner" class="nav-item">
          <router-link class="nav-link" :to="{ name: 'restaurants' }"
            >Restaurants</router-link
          >
        </li>
        <li v-if="authOwner" class="nav-item">
          <router-link class="nav-link" :to="{ name: 'meals' }"
            >Meals</router-link
          >
        </li>
        <li v-if="auth" class="nav-item">
          <router-link class="nav-link" :to="{ name: 'orders' }"
            >Orders</router-link
          >
        </li>
        </ul>
        <small v-if="auth" class="text-muted">
          <a href="#" @click="onLogout" class="nav-link"
            >Log Out <small>[{{user.email}}] <span v-show="authOwner">[owner]</span></small></a>
        </small>
      
    </div>
  </nav>
</template>

<script>
export default {
  name: "Menu",
  computed: {
    user() {
      return this.$store.getters["auth/user"];
    },
    auth() {
      return this.$store.getters["auth/ifAuth"];
    },
    authOwner() {
      return this.$store.getters["auth/ifAuthOwner"];
    },
  },
  methods: {
    onLogout() {
      this.$store.dispatch("auth/logout");
    },
  },
};
</script>

<style></style>
