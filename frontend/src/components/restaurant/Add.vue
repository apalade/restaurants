<template>
  <div class="submit-form">
    <div v-show="message" class="fixed-top alert alert-danger" role="alert">
        {{ message }}
    </div>
      <div class="form-group">
        <label for="name">Name</label>
        <input
          type="text"
          class="form-control"
          id="name"
          required
          v-model="restaurant.name"
          name="name"
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <input
          class="form-control"
          id="description"
          required
          v-model="restaurant.description"
          name="description"
        />
      </div>

      <button @click="saveRestaurant" id='button' class="btn btn-success">Submit</button>
      
    </div>

</template>

<script>
import RestaurantService from "@/services/RestaurantService";
import getErrMsg from "@/helpers"

export default {
  name: "RestaurantAdd",
  data() {
    return {
      restaurant: {
        name: "",
        description: "",
      },
      message: ""
    };
  },
  methods: {
    saveRestaurant() {
      if (this.restaurant.name == '' || this.restaurant.description == '') {
        this.$store.dispatch("msg/set", {msg: 'All fields required.', type: 'error'})
        return
      }

      var data = {
        name: this.restaurant.name,
        description: this.restaurant.description
      };

      RestaurantService.create(data)
        .then(() => {
          this.$router.push({name: 'restaurants'})
        })
        .catch((error) => {      
          this.$store.dispatch("msg/set", {msg: getErrMsg(error), type: 'error'})
        });
    },
    
  }
};
</script>

<style>
.submit-form {
  max-width: 300px;
  margin: auto;
}
</style>