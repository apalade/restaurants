<template>
<div class="submit-form">
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label for="email">Mail</label>
          <input type="email" class="form-control" id="email" v-model="email" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password"  class="form-control"  id="password" v-model="password" />
        </div>
        <div class="submit">
          <button class="btn btn-primary" type="submit">Submit</button>
        </div>
      </form>
    </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    onSubmit() {
      this.$store.dispatch("auth/login", {
        email: this.email,
        password: this.password,
      });
    },
  },
};
</script>

<style scoped></style>
