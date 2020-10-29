<template>

    <div class="submit-form">
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label for="email">Mail</label>
          <input type="email" id="email" class="form-control" v-model="email" />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" class="form-control" v-model="password" />
        </div>

        <div class="form-group">
          <label for="password">Re-enter password</label>
          <input type="password" id="password2" class="form-control" v-model="password2" />
        </div>
        <div class="form-group form-check">
          <label for="checkbox" class="form-check-label">
                      <input type="checkbox" class="form-check-input" id="owner" v-model="owner" />
Restaurant owner? 
</label>
        </div>
        <div v-show="get_error" class="alert alert-warning"> {{ get_error }}</div>

        <div v-show="!get_error" class="submit">
          <button class="btn btn-primary" type="submit">Submit</button>
        </div>
      </form>

</div>
  
</template>

<script>
import AuthService from "@/services/AuthService";
import router from "@/router";
import getErrMsg from "../../helpers"

export default {
  name: "Register",
  data() {
    return {
      email: "",
      password: "",
      password2: "",
      owner: false,
    };
  },
  methods: {
    onSubmit() {
      const data = {
        email: this.email,
        password: this.password,
        is_owner: this.owner,
      };
      AuthService.register(data)
        .then(() => {
          router.push("/login");
        })
        .catch((error) => {
          const payload = {
            msg: getErrMsg(error),
            type: 'error'
          }
          this.$store.dispatch('msg/set', payload);
        });
    },
  },
  computed: {
    get_error() {
      if (!this.email && !this.password && !this.password2) {
        return "";
      }

      const reg_email = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      if (!this.email || !reg_email.test(this.email)) {
        return "Please insert a valid e-mail";
      } else if (!this.password) {
        return "Please insert a password";
      } else if (this.password != this.password2) {
        return "Passwords do not match";
      }
      return "";
    },
  },
};
</script>

<style scoped></style>
