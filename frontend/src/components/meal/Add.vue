<template>
  <div class="submit-form">
    <div class="form-group">
      <label for="name">Name</label>
      <input
        type="text"
        class="form-control"
        id="name"
        required
        v-model="meal.name"
        name="name"
      />
    </div>

    <div class="form-group">
      <label for="description">Description</label>
      <input
        class="form-control"
        id="description"
        required
        v-model="meal.description"
        name="description"
      />
    </div>

    <div class="form-group">
      <label for="price">Price</label>
      <input
        class="form-control"
        id="price"
        required
        v-model="meal.price"
        name="price"
      />
    </div>
    <div class="form-group">
      <label for="price">Restaurant</label>
      <select
        v-model="meal.restaurant_id"
        class="form-control"
        id="restaurant_id"
        name="restaurant_id"
      >
        <option
          v-for="(el, idx) in restaurants"
          v-bind:key="idx"
          v-bind:value="el.id"
          >{{ el.name }}</option
        >

        />
      </select>
    </div>

    <button @click="saveMeal" class="btn btn-success" id="button">Submit</button>
  </div>
</template>

<script>
import MealService from "@/services/MealService";
import RestaurantService from "@/services/RestaurantService";
import getErrMsg from "@/helpers"

export default {
  name: "MealAdd",
  data() {
    return {
      meal: {
        name: "",
        description: "",
        price: null,
        restaurant_id: null,
      },
      restaurants: [],
      message: "",
      user: this.$store.getters["auth/user"],
    };
  },
  methods: {
    saveMeal() {
      if (
        this.meal.name == "" ||
        this.meal.description == "" ||
        this.meal.price == null ||
        this.meal.restaurant_id == null
      ) {
        this.$store.dispatch("msg/set", {
          msg: "Please make sure all fields are filled in.",
          type: "error",
        });

        return;
      }

      var data = {
        name: this.meal.name,
        description: this.meal.description,
        price: parseFloat(this.meal.price),
        restaurant_id: this.meal.restaurant_id,
      };

      MealService.create(data)
        .then(() => {
          this.$router.push({ name: "meals" });
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {
            msg: getErrMsg(error),
            type: "error",
          });
        });
    },

    getRestaurants(id) {
      RestaurantService.getAll(id)
        .then((response) => {
          this.restaurants = response.data;
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {
            msg: getErrMsg(error),
            type: "error",
          });
        });
    },
  },
  mounted() {
    this.getRestaurants(this.user.id);
  },
};
</script>

<style>

</style>
