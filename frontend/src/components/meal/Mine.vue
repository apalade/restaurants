<template>
  <div>
    <h2>
      My Meals
      
        <router-link class="btn btn-primary small" :to="{ name: 'meal-add' }"
          >Add
        </router-link>
    </h2>

    <div class="container">
      <div class="row">
        <div v-for="(el, idx) in meals" v-bind:key="idx" class="col-lg-3">
          <MealSingle
            :id="el.id"
            :img="img_link"
            :owner="true"
            :meal="el"
            :restaurant_id="el.restaurant.id"
            :restaurants="restaurants"
            v-on:deleteme="deleteMeal(idx)"
            v-on:editme="(data) => editMeal(idx, data)"
          />
        </div>
      </div>
    </div>

  
  </div>
</template>

<script>
import MealSingle from "@/components/meal/Single.vue";
import MealService from "@/services/MealService";
import RestaurantService from "@/services/RestaurantService";
import getErrMsg from "@/helpers";

export default {
  name: "MealMine",
  components: {
    MealSingle,
  },
  data() {
    return {
      user: this.$store.getters["auth/user"],
      img_link: "https://picsum.photos/400/200",
      meals: [],
      restaurants: [],
    };
  },
  methods: {
    getMeals(id) {
      MealService.getAll(id)
        .then((response) => {
          this.meals = response.data;
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {
            msg: getErrMsg(error),
            type: "error",
          });
        });
    },
    editMeal(idx, data) {
      data.meal.restaurant_id = data.restaurant_id
      MealService.update(data.meal)
        .then((response) => {
          this.$set(this.meals, idx, response.data);
        })
        .catch((error) => {
          this.$store.dispatch("msg/set", {
            msg: getErrMsg(error),
            type: "error",
          });
        });
    },
    deleteMeal(idx) {
      MealService.delete(this.meals[idx].id)
        .then(() => {
          this.meals.splice(idx, 1);
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
    this.getMeals(this.user.id);
    this.getRestaurants(this.user.id);
  },
};
</script>

<style>
body {
  background-color: #f4f4f4;
}
</style>
